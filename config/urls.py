from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path(f"admin/{settings.DJANGO_ADMIN_URL}/", admin.site.urls),
    path("", include("shop.urls", namespace="shop")),
    path("users/", include("users.urls", namespace="users")),
    path("payment/zarinpal/", include("zarinpal.urls", namespace="zarinpal")),
]
