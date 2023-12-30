from django.core.exceptions import ValidationError


def phone_number(value):
    if len(value) != 11:
        raise ValidationError(
            "Phone Number Must Be Exactly 11 characters Long")
    if not value.startswith("09"):
        raise ValidationError("Phone Number Must Start With '09'")
    if not value[2:].isdigit():
        raise ValidationError(
            "Phone Number Must Contain Only Numerical Digits")
