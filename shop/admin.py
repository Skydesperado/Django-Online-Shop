import csv
import datetime

from django.contrib import admin
from django.http import HttpResponse

from .models import Category, Discount, Order, OrderItem, Product


def export_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    content = "Attachment; File Name = {opts.verbose_name}.csv"
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = content
    writer = csv.writer(response)
    fields = [
        field for field in opts.get_fields()
        if not field.many_to_many and not field.one_to_many
    ]
    writer.writerow([field.verbose_name for field in fields])
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, str(field.name))
            if isinstance(value, datetime.datetime):
                value = value.strftime("%d/%m/%Y")
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_csv.short_description = "Export Selected Orders To CSV File"

admin.site.register(Category)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    raw_id_fields = ["category"]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ["product"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "is_paid", "updated_at"]
    list_filter = ["is_paid"]
    inlines = [OrderItemInline]
    actions = [export_csv]


admin.site.register(Discount)
