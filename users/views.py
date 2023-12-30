import random

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from utilities.sms import otp, welcome

from .forms import OTPForm, UserLoginForm, UserRegistrationForm
from .models import OTP, User


class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = "users/register.html"

    def get(self, request):
        form = self.form_class
        if request.user.is_authenticated:
            return redirect("shop:shop-view")
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(10000, 99999)
            otp(random_code, form.cleaned_data["phone_number"])
            OTP.objects.create(otp=random_code,
                               phone_number=form.cleaned_data["phone_number"])
            request.session["registration"] = {
                "first_name": form.cleaned_data["first_name"],
                "last_name": form.cleaned_data["last_name"],
                "phone_number": form.cleaned_data["phone_number"],
                "email": form.cleaned_data["email"],
                "password": form.cleaned_data["password"],
            }
            last_four_digits = form.cleaned_data["phone_number"][-4:]
            messages.success(
                request,
                f"We've Sent The Verification Code To The Phone Number Ending With {last_four_digits}, Please Check Your Messages",
                "success")
            return redirect("users:verify-view")
        return render(request, self.template_name, {"form": form})


class UserVerifyView(View):
    form_class = OTPForm

    def get(self, request):
        form = self.form_class()
        if request.user.is_authenticated:
            return redirect("shop:shop-view")
        return render(request, "users/verify.html", {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if "registration" not in request.session:
            return redirect("users:register-view")
        session = request.session["registration"]
        try:
            queryset = OTP.objects.get(phone_number=session["phone_number"])
        except OTP.DoesNotExist:
            messages.error(request, "Invalid Phone Number During Verification",
                           "danger")
            return redirect("users:register-view")
        if form.is_valid():
            clean_data = form.cleaned_data
            if clean_data["otp"] == queryset.otp:
                try:
                    User.objects.get(phone_number=session["phone_number"])
                except User.DoesNotExist:
                    User.objects.create_user(
                        first_name=session["first_name"],
                        last_name=session["last_name"],
                        phone_number=session["phone_number"],
                        email=session["email"],
                        password=session["password"])
                OTP.objects.filter(
                    phone_number=session["phone_number"]).delete()
                user = authenticate(request,
                                    phone_number=session["phone_number"],
                                    password=session["password"])
                if user is not None:
                    login(request, user)
                    welcome(session["phone_number"])
                    messages.success(request, "Registered Successfully!",
                                     "success")
                    return redirect("shop:shop-view")
                else:
                    messages.error(request,
                                   "Authentication failed, Please try again",
                                   "danger")
                    return redirect("users:verify-view")
            else:
                messages.error(request, "Invalid Code, Try Again", "danger")
                return redirect("users:verify-view")
        return redirect("shop:shop-view")


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = "users/login.html"

    def get(self, request):
        form = self.form_class
        if request.user.is_authenticated:
            return redirect("shop:shop-view")
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            user = authenticate(request,
                                phone_number=clean_data["phone_number"],
                                password=clean_data["password"])
            if user is not None:
                login(request, user)
                messages.success(request, "Logged In Successfully!", "success")
                return redirect("shop:shop-view")
            messages.error(request, "Phone Number Or Password Is Wrong",
                           "danger")
        return render(request, self.template_name, {"form": form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, "Logged Out", "success")
        return redirect("shop:shop-view")
