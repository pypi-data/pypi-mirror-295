from django.contrib import admin
from .models import VobapayTransaction, VobapayResponse


class ResponseInline(admin.StackedInline):
    model = VobapayResponse
    fields = (
    'created_at', 'transaction', 'response_code', 'response_msg', 'raw_response', 'request_url', 'request_data',)
    readonly_fields = fields
    extra = 0
    can_delete = False


class VobapayTransactionAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'merchant_tx_id', 'reference', 'latest_response_code',)
    ordering = ('-created_at',)
    fields = ('created_at', 'merchant_tx_id', 'reference', 'amount', 'purpose', 'redirect_url', 'notify_url', 'success_url', 'error_url',)
    search_fields = ('merchant_tx_id', 'reference')
    readonly_fields = fields
    inlines = [ResponseInline]


class VobapayResponseAdmin(admin.ModelAdmin):
    list_display = ('transaction', 'response_code', 'response_msg',)
    ordering = ('-created_at',)
    fields = ('created_at', 'transaction', 'response_code', 'response_msg', 'raw_response', 'request_url', 'request_data',)
    search_fields = ('transaction__merchant_tx_id', 'response_code', 'response_msg',)
    readonly_fields = fields


admin.site.register(VobapayTransaction, VobapayTransactionAdmin)
admin.site.register(VobapayResponse, VobapayResponseAdmin)
