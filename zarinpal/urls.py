from django.urls import path

from .views import *

app_name = "zarinpal"

urlpatterns = [
    path("request/<int:order_id>/",
         PaymentRequestView.as_view(),
         name="payment-request-view"),
    path("verify/", PaymentVerifyView.as_view(), name="payment-verify-view"),
]
