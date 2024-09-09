from __future__ import unicode_literals

import logging

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django_vobapay import settings as django_vobapay_settings
from django_vobapay.constants import RESULT_PAYMENT_STATUS


@python_2_unicode_compatible
class VobapayTransaction(models.Model):
    created_at = models.DateTimeField(_("created_at"), auto_now_add=True)

    reference = models.TextField(_("reference"), null=True)
    backend_tx_id = models.TextField(_("backend tx id"), null=True)
    merchant_tx_id = models.CharField(_("merchant tx id"), max_length=255, unique=True)

    merchant_id = models.IntegerField(_("Merchant ID"))
    project_id = models.IntegerField(_("Project ID"))

    amount = models.PositiveIntegerField(_("amount in Cents"))
    currency = models.CharField(_("Currency Code (3 Chars)"), max_length=3, default='EUR')
    purpose = models.CharField(_("purpose"), max_length=27)

    redirect_url = models.TextField(_("redirect url"))
    notify_url = models.TextField(_("notify url"))
    success_url = models.TextField(_("success url"))
    error_url = models.TextField(_("error url"))

    payment_type = models.CharField(_("paymentname"), max_length=128)

    result_payment = models.IntegerField(_("return code from vobapay transaction"), null=True)

    objects = models.Manager()

    def __str__(self):
        return self.merchant_tx_id

    @property
    def valid_payment(self) -> bool:
        return self.result_payment in django_vobapay_settings.VOBAPAY_VALID_TRANSACTION_STATUSES

    def refresh_from_vobapay(self, vobapay_wrapper) -> bool:
        """
        :param vobapay_wrapper: VobapayWrapper
        :return: bool; True if state is successfully updated
        """
        return vobapay_wrapper.update_transaction_state(self)

    class Meta:
        verbose_name = _("Vobapay Transaction")
        verbose_name_plural = _("Vobapay Transactions")

    @property
    def latest_response_code(self):
        if self.responses.exists():
            return self.responses.latest().response_code
        return None

    @property
    def latest_response_msg(self):
        if self.responses.exists():
            return self.responses.latest().response_msg
        return None


@python_2_unicode_compatible
class VobapayResponse(models.Model):
    created_at = models.DateTimeField(_("created_at"), auto_now_add=True)
    transaction = models.ForeignKey(VobapayTransaction, on_delete=models.CASCADE, related_name='responses')
    response_code = models.IntegerField(_("rc field from vobapay response"), null=True)
    response_msg = models.TextField(_("msg field from vobapay response"), null=True)
    raw_response = models.TextField(_("raw response"), null=True)
    # original request url & data that caused the response
    request_url = models.CharField(_("Request url"), max_length=255, null=True, blank=True)
    request_data = models.TextField(_("Request data"), null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        return f"Response {self.id} - code: {RESULT_PAYMENT_STATUS.get(self.response_code, str(self.response_code) + ' Unknown')}"

    class Meta:
        verbose_name = _("Vobapay Response")
        verbose_name_plural = _("Vobapay Responses")
        ordering = ['-created_at']
        get_latest_by = 'created_at'