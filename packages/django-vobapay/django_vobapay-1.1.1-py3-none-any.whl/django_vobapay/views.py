import logging
from collections import OrderedDict

from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View, RedirectView

from django_vobapay.constants import RESULT_PAYMENT_STATUS
from django_vobapay.models import VobapayTransaction, VobapayResponse

from django_vobapay.wrappers import VobapayWrapper

import django_vobapay.wrappers as wrappers
from django_vobapay import settings as django_vobapay_settings

logger = logging.getLogger(__name__)


def validate_vobapay_get_params(vobapay_wrapper, get_params):
    desired_variables = ['gcReference', 'gcMerchantTxId', 'gcBackendTxId', 'gcAmount', 'gcCurrency', 'gcResultPayment', 'gcHash']

    # check for expected parameters
    if not all([var in get_params for var in desired_variables]):
        logger.error(
            _("Not all desired variables where part of the Vobapay Notification. Payload: {}").format(str(get_params))
        )
        return False

    return True


class NotifyVobapayView(View):
    vobapay_wrapper = VobapayWrapper()

    def get(self, request, *args, **kwargs):

        get_params = OrderedDict()
        # creating OrderedDict out of query string, because we need it ordered for the hash check
        for query_param in request.META['QUERY_STRING'].split('&'):
            get_params[query_param.split('=')[0]] = "=".join(query_param.split('=')[1:])

        if not validate_vobapay_get_params(self.vobapay_wrapper, get_params):
            return HttpResponse(status=400)

        try:
            vobapay_transaction = VobapayTransaction.objects.get(reference=get_params['gcReference'])
        except VobapayTransaction.DoesNotExist:
            return HttpResponse(status=400)

        vobapay_transaction.result_payment = int(get_params['gcResultPayment'])
        vobapay_transaction.backend_tx_id = get_params['gcBackendTxId']
        vobapay_transaction.save()

        VobapayResponse.objects.create(
            transaction=vobapay_transaction,
            response_code=get_params['gcResultPayment'],
            raw_response=str(request.GET.dict()),
            request_url=request.path,
        )

        return self.handle_updated_transaction(vobapay_transaction=vobapay_transaction)

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(NotifyVobapayView, self).dispatch(request, *args, **kwargs)

    def handle_updated_transaction(self, vobapay_transaction, expected_statuses=django_vobapay_settings.VOBAPAY_VALID_TRANSACTION_STATUSES):
        """
            Override to use the vobapay_transaction in the way you want.
        """
        if vobapay_transaction.result_payment not in expected_statuses:
            logger.error(
                _("Vobapay Result faulty: {}").format(RESULT_PAYMENT_STATUS.get(vobapay_transaction.result_payment, vobapay_transaction.result_payment))
            )
            return HttpResponse(status=400)
        return HttpResponse(status=200)


class VobapayReturnView(RedirectView):
    vobapay_wrapper = wrappers

    def get_error_url(self):
        return django_vobapay_settings.VOBAPAY_ERROR_URL

    def get_cancel_url(self, vobapay_transaction):
        return vobapay_transaction.error_url

    def get_success_url(self, vobapay_transaction):
        return vobapay_transaction.success_url

    def get_redirect_url(self, *args, **kwargs):
        # creating OrderedDict out of query string, because we need it ordered for the hash check
        get_params = OrderedDict()
        for query_param in self.request.META['QUERY_STRING'].split('&'):
            get_params[query_param.split('=')[0]] = "=".join(query_param.split('=')[1:])

        if not validate_vobapay_get_params(self.vobapay_wrapper, get_params):
            return self.get_error_url()

        try:
            vobapay_transaction = VobapayTransaction.objects.get(reference=get_params['gcReference'])
        except VobapayTransaction.DoesNotExist:
            logger.error('vobapay transaction does not exist')
            return self.get_error_url()

        vobapay_transaction.result_payment = int(get_params['gcResultPayment'])
        vobapay_transaction.backend_tx_id = get_params['gcBackendTxId']
        vobapay_transaction.save()

        VobapayResponse.objects.create(
            transaction=vobapay_transaction,
            response_code=get_params['gcResultPayment'],
            raw_response=str(self.request.GET.dict()),
            request_url=self.request.path,
        )

        if not vobapay_transaction.valid_payment:
            return self.get_cancel_url(vobapay_transaction)
        return self.get_success_url(vobapay_transaction)
