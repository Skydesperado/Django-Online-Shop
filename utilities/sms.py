import ghasedakpack
from django.conf import settings


def otp(otp, phone_number):
    sms = ghasedakpack.Ghasedak(settings.GHASEDAK_API_KEY)
    sms.send({
        "message": f"Verification Code: {otp}",
        "receptor": phone_number,
        "linenumber": ""
    })


def welcome(phone_number):
    sms = ghasedakpack.Ghasedak(settings.GHASEDAK_API_KEY)
    sms.send({
        "message": "Welcome To Django-Online-Shop!",
        "receptor": phone_number,
        "linenumber": ""
    })
