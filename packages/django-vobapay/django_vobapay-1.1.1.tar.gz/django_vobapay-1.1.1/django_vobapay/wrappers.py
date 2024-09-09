import logging
from typing import Optional
import uuid
import requests
from collections import OrderedDict
from django.utils.translation import gettext_lazy as _, ugettext

from django_vobapay.models import VobapayResponse
from django_vobapay.settings import *

logger = logging.getLogger(__name__)


class VobapayWrapper(object):
    """
    vobapay api integration
    """
    interface_version = 'django_vobapay_v{}'.format(DJANGO_VOBAPAY_VERSION)

    api_url = None
    sandbox = True

    payment = None
    payment_type = None

    def __init__(self, payment=None):
        """
        initial
        :param payment: object with auth and paymenttype should contain PROJECT_ID, TYPE, PROJECT_PASSWORD, MERCHANT_ID
        """
        super(VobapayWrapper, self).__init__()

        try:
            if payment:
                self.payment = payment
                self.payment_type = self.payment.get('TYPE')
                self.sandbox = self.payment.get('SANDBOX', True)
            else:
                return None
        except:
            pass

    def _get_hash_for_payload(self, payload):
        """
        generates hash for vobapay requests
        :param payload:
        :return: string
        """
        return ''.join(map(str, [value for value in payload.values()]))

    def _generate_hash_from_dict(self, data_dict):
        """
        generates hash for api call
        :param data_dict:
        :return:
        """
        import hashlib
        import hmac
        data_string = "".join([str(val) for val in data_dict.values()])
        data_hash = hmac.new(self.payment['PROJECT_PASSWORD'], "{}".format(data_string).encode("utf-8"),
                             hashlib.md5).hexdigest()
        return data_hash

    def _generate_hash_from_text(self, data_text):
        """
        gerenerates hash for response object text
        :param data_text:
        :return:
        """
        import hashlib
        import hmac
        data_hash = hmac.new(self.payment['PROJECT_PASSWORD'], data_text.encode("utf-8"), hashlib.md5).hexdigest()
        return data_hash

    def start_transaction(self,
                          merchant_tx_id: str, 
                          amount: int, 
                          purpose: Optional[str] = None,
                          currency: str = 'EUR',
                          redirect_url: str = VOBAPAY_RETURN_URL,
                          notify_url: str = VOBAPAY_NOTIFICATION_URL,
                          success_url: str = VOBAPAY_SUCCESS_URL,
                          error_url: str = VOBAPAY_ERROR_URL,
                          optional_data: Optional[dict] = None):
        """
        vobapay transaction. The data needs to be ordered like in the API docs, otherwise the hash will be invalid.
        :param merchant_tx_id:
        :param amount:
        :param purpose:
        :param currency:
        :param redirect_url:
        :param notify_url:
        :param success_url:
        :param error_url:
        :param optional_data: None or (ordered) dict with additional parameters to send to Vobapay
        :return: response dict from vobapay
        """

        if not purpose:
            purpose = str(uuid.uuid4())

        if not optional_data:
            optional_data = dict()

        # currently the required data is the same for all payment methods.
        data = OrderedDict()
        data['merchantId'] = self.payment.get('MERCHANT_ID')
        data['projectId'] = self.payment.get('PROJECT_ID')
        data['merchantTxId'] = merchant_tx_id
        data['amount'] = amount
        data['currency'] = currency
        data['purpose'] = purpose
        data['urlRedirect'] = redirect_url
        data['urlNotify'] = notify_url

        data.update(optional_data)

        # make api call with given data
        response = self.call_api(url=VOBAPAY_API_URL(self.sandbox), data=data)

        response_hash = response.headers.get('hash')
        response_dict = response.json()
        response_text = response.text

        generated_hash = self._generate_hash_from_text(response_text)
        # check if hash is valid
        assert response_hash == generated_hash, _("Response hash {} not compatible with the generated hash {}.").format(response_hash, generated_hash)

        if response_dict.get('reference'):
            # generate transaction object
            from django_vobapay.models import VobapayTransaction
            vobapay_transaction = VobapayTransaction()
            vobapay_transaction.redirect_url = redirect_url
            vobapay_transaction.notify_url = notify_url
            vobapay_transaction.success_url = success_url
            vobapay_transaction.error_url = error_url
            vobapay_transaction.project_id = self.payment.get('PROJECT_ID')
            vobapay_transaction.merchant_id = self.payment.get('MERCHANT_ID')
            vobapay_transaction.merchant_tx_id = merchant_tx_id
            vobapay_transaction.amount = amount
            vobapay_transaction.currency = currency
            vobapay_transaction.purpose = purpose
            vobapay_transaction.reference = response_dict.get('reference')
            vobapay_transaction.payment_type = self.payment_type
            vobapay_transaction.save()
            VobapayResponse.objects.create(
                transaction=vobapay_transaction,
                response_code=response_dict.get('rc'),
                response_msg=response_dict.get('msg'),
                raw_response=str(response.__dict__),
                request_url=VOBAPAY_API_URL(self.sandbox),
                request_data=str(data),
            )
        else:
            logger.error(_("no reference given by response"))
            return None
        return response_dict

    def update_transaction_state(self, vobapay_transaction) -> bool:
        """

        :param vobapay: VobapayTransaction
        :return: bool; True if state is successfully updated
        """
        data = OrderedDict()
        data['merchantId'] = vobapay_transaction.merchant_id
        data['projectId'] = vobapay_transaction.project_id
        data['reference'] = vobapay_transaction.reference
        response = self.call_api(url=VOBAPAY_API_STATUS_URL(self.sandbox), data=data)
        response_hash = response.headers.get('hash')
        response_dict = response.json()
        response_text = response.text

        generated_hash = self._generate_hash_from_text(response_text)
        # check if hash is valid
        assert response_hash == generated_hash, _("Response hash {} not compatible with the generated hash {}. Related reference: {}").format(response_hash, generated_hash, vobapay_transaction.reference)

        VobapayResponse.objects.create(
            transaction=vobapay_transaction,
            response_code=response_dict.get('rc'),
            response_msg=response_dict.get('msg'),
            raw_response=str(response.__dict__),
            request_url=VOBAPAY_API_STATUS_URL(self.sandbox),
            request_data=str(data),
        )
        if response_dict.get('rc') == 0:
            update_fields = ["backend_tx_id", "result_payment"]
            vobapay_transaction.backend_tx_id = response_dict.get('backendTxId', None)
            vobapay_transaction.result_payment = int(response_dict.get('resultPayment', None))
            vobapay_transaction.save(update_fields=update_fields)

        return response_dict.get('rc') == 0

    def call_api(self, url=None, data=None):
        """
        call vobapay api
        :param url: http url of api endpoint
        :param data: dataobject as OrderedDict
        :return: response object
        """

        if not self.payment:
            return False
        if not url.lower().startswith('http'):
            url = '{0}{1}'.format(self.api_url, url)

        generated_hash = self._generate_hash_from_dict(data)
        data.update({'hash': generated_hash})

        try:
            response = requests.post(url, data=data)
        except requests.HTTPError as e:
            logger = logging.getLogger(__name__)
            if hasattr(e, 'errno'):
                logger.error("Vobapay Error {0}({1})".format(e.errno, e.strerror))
            else:
                logger.error(
                    "Vobapay Error({0})".format(e.strerror))
        else:
            return response
        return False
