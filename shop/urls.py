from django.conf import settings
from django.urls import include, path

from .views import (BucketObjectDeleteView, BucketObjectDownloadView,
                    BucketView, CartAddView, CartRemoveView, CartView,
                    DiscountView, OrderCreateView, OrderDetailView,
                    ProductDetailView, ShopView)

app_name = "shop"

bucket = [
    path("", BucketView.as_view(), name="bucket-view"),
    path(f"<str:key>/{settings.BUCKET_DELETE_URL}/",
         BucketObjectDeleteView.as_view(),
         name="bucket-object-delete-view"),
    path(f"<str:key>/{settings.BUCKET_DOWNLOAD_URL}/",
         BucketObjectDownloadView.as_view(),
         name="bucket-object-download-view"),
]

urlpatterns = [
    path("", ShopView.as_view(), name="shop-view"),
    path("category/<slug:category>/", ShopView.as_view(),
         name="category-view"),
    path("cart/", CartView.as_view(), name="cart-view"),
    path("cart/add/<int:product_id>/<slug:slug>/",
         CartAddView.as_view(),
         name="cart-add-view"),
    path("cart/remove/<int:product_id>/",
         CartRemoveView.as_view(),
         name="cart-remove-view"),
    path("order/detail/<int:order_id>/",
         OrderDetailView.as_view(),
         name="order-detail-view"),
    path("order/create/", OrderCreateView.as_view(), name="order-create-view"),
    path("order/discount/<int:order_id>/",
         DiscountView.as_view(),
         name="discount-view"),
    path(f"{settings.BUCKET_URL}/", include(bucket)),
    path("<slug:slug>/", ProductDetailView.as_view(), name="product-view"),
]
