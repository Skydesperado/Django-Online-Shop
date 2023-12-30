from django.urls import path

from .views import *

app_name = "users"

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register-view"),
    path("verify/", UserVerifyView.as_view(), name="verify-view"),
    path("login/", UserLoginView.as_view(), name="login-view"),
    path("logout/", UserLogoutView.as_view(), name="logout-view"),
]
