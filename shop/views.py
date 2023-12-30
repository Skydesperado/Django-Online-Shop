import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from utilities.permissions import IsAdminMixin, IsAdminOrOwnerMixin

from .cart import Cart
from .forms import CartAddForm, DiscountForm
from .models import Category, Discount, Order, OrderItem, Product
from .tasks import (delete_bucket_object_task, download_bucket_object_task,
                    get_bucket_objects_task)


class ShopView(View):
    def get(self, request, category=None):
        products = Product.objects.filter(is_available=True)
        categories = Category.objects.filter(is_sub_category=False)
        try:
            category = Category.objects.get(slug=category)
            products = products.filter(category=category)
        except Category.DoesNotExist:
            pass
        return render(request, "shop/shop.html", {
            "products": products,
            "categories": categories
        })


class ProductDetailView(View):
    def get(self, request, slug):
        form = CartAddForm()
        product = get_object_or_404(Product, slug=slug)
        return render(request, "shop/detail.html", {
            "product": product,
            "form": form
        })


class CartView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, "shop/cart.html", {"cart": cart})


class CartAddView(View):
    form_class = CartAddForm

    def post(self, request, product_id, slug):
        form = self.form_class(request.POST)
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        if form.is_valid():
            cart.add(product, form.cleaned_data["quantity"])
        return redirect("shop:product-view", product.slug)


class CartRemoveView(View):
    def get(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect("shop:cart-view")


class OrderDetailView(LoginRequiredMixin, IsAdminOrOwnerMixin, View):
    form_class = DiscountForm

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        return render(request, "shop/order.html", {
            "order": order,
            "form": self.form_class
        })


class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        if not cart:
            messages.warning(request,
                             "Your Cart Is Empty, Add Items Before Checkout")
            return redirect("shop:cart-view")
        order = Order.objects.create(user=request.user)
        OrderItem.objects.bulk_create([
            OrderItem(order=order,
                      product=item["product"],
                      price=float(item["price"]),
                      quantity=item["quantity"]) for item in cart
        ])
        cart.clear()
        return redirect("shop:order-detail-view", order.id)


class DiscountView(LoginRequiredMixin, View):
    form_class = DiscountForm

    def post(self, request, order_id):
        form = self.form_class(request.POST)
        now = datetime.datetime.now()
        if form.is_valid():
            code = form.cleaned_data["code"]
            try:
                coupon = Discount.objects.get(code__exact=code,
                                              valid_from__lte=now,
                                              valid_until__gte=now,
                                              active=True)
            except Discount.DoesNotExist:
                messages.error(request, "Coupon Does Not Exist", "danger")
                return redirect("orders:order-detail", order_id)
            order = get_object_or_404(Order, id=order_id)
            order.discount = coupon.discount
            order.save()
            return redirect("shop:order-detail-view", order_id)


class BucketView(IsAdminMixin, View):
    template_name = "shop/bucket.html"

    def get(self, request):
        objects = get_bucket_objects_task()
        return render(request, self.template_name, {"objects": objects})


class BucketObjectDownloadView(IsAdminMixin, View):
    def get(self, request, key):
        if download_bucket_object_task.delay(key):
            messages.success(request, "Object Will Be Download", "success")
            return redirect("shop:bucket-view")
        else:
            return redirect("shop:bucket-view")


class BucketObjectDeleteView(IsAdminMixin, View):
    def get(self, request, key):
        if delete_bucket_object_task.delay(key):
            messages.success(request, "Object Will Be Delete", "success")
            return redirect("shop:bucket-view")
        else:
            return redirect("shop:bucket-view")
