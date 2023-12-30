import json

import requests
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views import View

from shop.models import Order
from utilities.permissions import IsUserCreatedOrderMixin

if settings.SANDBOX:
    sandbox = "sandbox"
else:
    sandbox = "www"

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

description = "Payment For Uour Order On  Django-Online-Shop"

CallbackURL = f"http://{settings.DOMAIN}/payment/zarinpal/verify/"


class PaymentRequestView(LoginRequiredMixin, IsUserCreatedOrderMixin, View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        request.session["payment_request"] = {
            "order_id": order.id,
        }
        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": order.get_total_price(),
            "Description": description,
            "Phone": request.user.phone_number,
            "CallbackURL": CallbackURL,
        }
        data = json.dumps(data)
        headers = {
            "content-type": "application/json",
            "content-length": str(len(data))
        }
        try:
            response = requests.post(ZP_API_REQUEST,
                                     data=data,
                                     headers=headers,
                                     timeout=10)
            if response.status_code == 200:
                response = response.json()
                if response["Status"] == 100:
                    return {
                        "status": True,
                        "url": ZP_API_STARTPAY + str(response["Authority"]),
                        "authority": response["Authority"]
                    }
                else:
                    return {"status": False, "code": str(response["Status"])}
            return response
        except requests.exceptions.Timeout:
            return {"status": False, "code": "timeout"}
        except requests.exceptions.ConnectionError:
            return {"status": False, "code": "connection error"}


class PaymentVerifyView(LoginRequiredMixin, IsUserCreatedOrderMixin, View):
    def get(self, request):
        order_id = request.session["payment_request"]["order_id"]
        order = Order.objects.get(id=int(order_id))
        authority = request.GET.get("Authority")
        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": order.get_total_price(),
            "Authority": authority,
        }
        data = json.dumps(data)
        headers = {
            "content-type": "application/json",
            "content-length": str(len(data))
        }
        response = requests.post(ZP_API_VERIFY, data=data, headers=headers)
        if response.status_code == 200:
            response = response.json()
            if response["Status"] == 100:
                order.paid = True
                order.save()
                return {"status": True, "RefID": response["RefID"]}
            else:
                return {"status": False, "code": str(response["Status"])}
        return response
