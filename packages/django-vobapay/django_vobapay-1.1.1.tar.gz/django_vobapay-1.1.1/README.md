Django Vobapay
============================

Implementation of [Vobapay API](https://www.vobapay.de).
The following doc explain how to set up the Vobapay API for django.

## How to install django-vobapay?

There are just two steps needed to install django-vobapay:

1. Install django-vobapay to your virtual env:

	```bash
	pip install django-vobapay
	```

2. Configure your django installation with the following lines:

	```python
    # django-vobapay
    INSTALLED_APPS += ('django_vobapay', )

	```

    There is a list of other settings you could set down below.

3. Include the notification View in your URLs:

	```python
    # urls.py
    from django.conf.urls import include, url

    urlpatterns = [
        url('^vobapay/', include('django_vobapay.urls')),
    ]
	```

## What do you need for django-vobapay?

1. An merchant account for Vobapay
2. Django >= 2.2

## Usage

VobapayWrapper acts as the interface to the Vobapay API. It provides methods to start a transaction and to check the status of a transaction.

Note that `SANDBOX` is enabled by default. Please set it to `False` in order to use the live system.

### Code example:

```python
from django_vobapay.wrappers import VobapayWrapper
vobapay_wrapper = VobapayWrapper()

vobapay_wrapper = VobapayWrapper(
	payment={
		'MERCHANT_ID': '123456',
		'PROJECT_ID': '1010',
		'PROJECT_PASSWORD': bytes('some-pass', encoding='UTF-8'),
		'TYPE': 'PAYPAL',
		'SANDBOX': False,
	}
)

vobapay_transaction = vobapay_wrapper.start_transaction(
	merchant_tx_id=uuid.uuid4(),
	amount=amount_in_cents,  # 1000 = 10.00 €
	purpose='payment for something',
	redirect_url=redirect_url, # url to your view that inherits VobapayReturnView
	notify_url=notification_url, # url to your view that inherits NotifyVobapayView
	error_url=cancelled_url, # url to your error page if the payment is cancelled
	success_url=success_url, # url to your success page if the payment is successful
)
if vobapay_transaction is not False:
	# might want to save vobapay_transaction['reference'] to your database
	# return the redirect url to the user
	return redirect(vobapay_transaction['redirect'])
```

Normally the payment result should be available in the `VobapayReturnView` view. 
In case the user clsoed the window before the rediect went through, Vobapay will also send a notification to the `NotifyVobapayView` view.

In the `VobapayReturnView` view you can overwrite the following functions to handle different results:

```python
class MyVobapayReturnView(VobapayReturnView):
	def get_error_url(self):
		# your code here
		return django_vobapay_settings.VOBAPAY_ERROR_URL
	
	def get_cancel_url(self, vobapay_transaction):
		# your code here
		return vobapay_transaction.error_url
	
	def get_success_url(self, vobapay_transaction):
		# your code here
		return vobapay_transaction.success_url
```

Similarly in the `NotifyVobapayView` view you can overwrite the following functions to handle different results:

```python
class MyNotifyVobapayView(NotifyVobapayView):
	def handle_updated_transaction(self, vobapay_transaction, expected_statuses=django_vobapay_settings.VOBAPAY_VALID_TRANSACTION_STATUSES):
        if vobapay_transaction.result_payment not in expected_statuses:
			# your error hadnling here
            logger.error(
                _("Vobapay Result faulty: {}").format(RESULT_PAYMENT_STATUS[vobapay_transaction.result_payment] if vobapay_transaction.result_payment in RESULT_PAYMENT_STATUS else vobapay_transaction.result_payment)
            )
            return HttpResponse(status=400)
		# your success handling here
        return HttpResponse(status=200)
```

### Checking the status of a transaction

If you want to write a function to check the status of a transaction, you can use the following code:

```python
from django_vobapay.models import VobapayTransaction
from django_vobapay.wrappers import VobapayWrapper
from django_vobapay.settings import VOBAPAY_VALID_TRANSACTION_STATUSES

vobapay_transaction = VobapayTransaction.objects.get(reference='123456')
vobapay_wrapper = VobapayWrapper(
	payment={
		'MERCHANT_ID': '123456',
		'PROJECT_ID': '1010',
		'PROJECT_PASSWORD': bytes('some-pass', encoding='UTF-8'),
		'SANDBOX': True,
	}
)
vobapay_transaction.refresh_from_vobapay(vobapay_wrapper=vobapay_wrapper)

if vobapay_transaction.result_payment not in VOBAPAY_VALID_TRANSACTION_STATUSES:
	# something went wrong. See:
	# vobapay_transaction.latest_response_code
	# vobapay_transaction.latest_response_msg
	return False
# payment was successful
return True
```


## Copyright and license

Copyright 2024 Particulate Solutions GmbH, under [MIT license](https://github.com/ParticulateSolutions/django-vobapay/blob/master/LICENSE).