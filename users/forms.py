from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import OTP, User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password",
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone_number", "email"]

    def clean_password2(self):
        clean_data = self.cleaned_data
        if clean_data["password1"] and clean_data["password2"]:
            if clean_data["password1"] == clean_data["password2"]:
                return clean_data["password2"]
            else:
                raise ValidationError("Passwords Doesn't Match")
        else:
            raise ValidationError("Please Enter Both Passwords")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text=
        "You Can Change Your Password Using This <a href=\"../password/\">Form</a>"
    )

    class Meta:
        model = User
        fields = [
            "first_name", "last_name", "phone_number", "email", "password",
            "last_login"
        ]


class UserRegistrationForm(forms.Form):
    first_name = forms.CharField(label="First Name", max_length=255)
    last_name = forms.CharField(label="Last Name", max_length=255)
    phone_number = forms.CharField(label="Phone Number", max_length=11)
    email = forms.EmailField()
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirm Password",
                                       widget=forms.PasswordInput)

    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]
        OTP.objects.filter(phone_number=phone_number).delete()
        if User.objects.filter(phone_number=phone_number).exists():
            raise ValidationError("This Phone Number Already Exists")
        return phone_number

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise ValidationError("This Email Already Exists")
        return email

    def clean_confirm_password(self):
        password = self.cleaned_data["password"]
        confirm_password = self.cleaned_data["confirm_password"]
        if password and confirm_password:
            if password == confirm_password:
                return confirm_password
            else:
                raise ValidationError("Passwords Doesn't Match")
        else:
            raise ValidationError("Please Enter Both Passwords")


class UserLoginForm(forms.Form):
    phone_number = forms.CharField(label="Phone Number", max_length=11)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class OTPForm(forms.Form):
    otp = forms.IntegerField(label="Code")
