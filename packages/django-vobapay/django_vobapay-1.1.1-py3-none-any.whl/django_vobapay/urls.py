from django.conf.urls import url

from django_vobapay.views import NotifyVobapayView, VobapayReturnView

urlpatterns = [
    url(r'^notify/$', NotifyVobapayView.as_view(), name='notify'),
    url(r'^return/$', VobapayReturnView.as_view(), name='return'),
]
