from django.urls import path
from .views import CreatePaymentIntent, payment_page, stripe_webhook, webhook_test_page, PaymentStatusAPI, payment_status_page

urlpatterns = [
    path("", payment_page, name="payment_page"),
    path("status/", payment_status_page, name="payment_status_page"),
    path("test-webhook/", webhook_test_page, name="webhook_test_page"),
    path("api/payments/", PaymentStatusAPI.as_view(), name="payment_status_api"),
    path("create-payment-intent/", CreatePaymentIntent.as_view(), name="create-payment-intent"),
    path("webhook/", stripe_webhook, name="stripe-webhook"),
]
