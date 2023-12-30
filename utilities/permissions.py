from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy

from shop.models import Order


class IsAdminMixin(UserPassesTestMixin):
    login_url = reverse_lazy("users:login-view")

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin


class IsAdminOrOwnerMixin(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_staff:
            return True
        order_id = self.kwargs.get("order_id")
        if order_id is None:
            messages.error(self.request, "Order ID Not Found", "danger")
        order = get_object_or_404(Order, id=order_id)
        if order.user == self.request.user:
            return True
        else:
            messages.error(self.request, "You Are Not The Owner of This Order",
                           "danger")
            return False


class IsUserCreatedOrderMixin(UserPassesTestMixin):
    def test_func(self):
        if Order.objects.filter(user=self.request.user).exists():
            return True
        else:
            messages.warning(self.request, "Create an Order", "warning")
            return False

    def handle_no_permission(self):
        return redirect("shop:shop-view")
