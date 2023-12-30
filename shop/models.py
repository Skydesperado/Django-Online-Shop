from ckeditor.fields import RichTextField
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name")
    sub_category = models.ForeignKey("self",
                                     on_delete=models.CASCADE,
                                     blank=True,
                                     null=True,
                                     related_name="sub_categories",
                                     verbose_name="Sub Category")
    is_sub_category = models.BooleanField(default=False,
                                          verbose_name="Sub Category")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Slug")

    class Meta:
        ordering = ["name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def get_absolute_url(self):
        return reverse("shop:category-view", args=[self.slug])

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name")
    description = RichTextField(verbose_name="Description")
    price = models.DecimalField(max_digits=7,
                                decimal_places=2,
                                verbose_name="Price")
    image = models.ImageField(verbose_name="Image")
    category = models.ManyToManyField(Category,
                                      related_name="products",
                                      verbose_name="Category")
    is_available = models.BooleanField(default=True, verbose_name="Available")
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Slug")

    class Meta:
        ordering = ["name"]
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def get_absolute_url(self):
        return reverse("shop:product-view", args=[self.slug])

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.PROTECT,
                             related_name="orders",
                             verbose_name="User")
    is_paid = models.BooleanField(default=False, verbose_name="Paid")
    discount = models.IntegerField(default=None,
                                   blank=True,
                                   null=True,
                                   verbose_name="Discount")
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        ordering = ["is_paid", "-updated_at"]
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def get_total_price(self):
        total = sum([item.get_cost() for item in self.order_items.all()])
        if self.discount:
            discount_price = (self.discount / 100) * total
            return int(total - discount_price)
        return total

    def __str__(self):
        return f"{self.user} - {str(self.id)}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              on_delete=models.PROTECT,
                              related_name="order_items",
                              verbose_name="Order")
    product = models.ForeignKey(Product,
                                on_delete=models.PROTECT,
                                related_name="order_items",
                                verbose_name="Product")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantity")
    price = models.PositiveIntegerField(verbose_name="Price")

    class Meta:
        verbose_name = "OrderItem"
        verbose_name_plural = "OrderItems"

    def get_cost(self):
        return float(self.price * self.quantity)

    def __str__(self):
        return f"{self.order} - {self.product} - {self.quantity}"


class Discount(models.Model):
    code = models.CharField(max_length=30, unique=True, verbose_name="Code")
    valid_from = models.DateTimeField(verbose_name="Valid From")
    valid_until = models.DateTimeField(verbose_name="Valid Until")
    discount = models.IntegerField(
        validators=[MinValueValidator(0),
                    MaxValueValidator(99)],
        verbose_name="Discount")
    is_active = models.BooleanField(default=False, verbose_name="Active")

    class Meta:
        verbose_name = "Discount"
        verbose_name_plural = "Discounts"

    def __str__(self):
        return self.code
