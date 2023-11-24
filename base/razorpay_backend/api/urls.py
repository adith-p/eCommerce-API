from django.urls import path
from .views import RazorpayStartPayment, RazorpayPaymentSuccess

urlpatterns = [
    path('pay/', RazorpayStartPayment.as_view(), name="payment"),
    path('payment/success/', RazorpayPaymentSuccess.as_view(), name="payment_success")
]
