from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserChangeForm, UserCreationForm
from .models import OTP, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = [
        "phone_number",
        "email",
        "first_name",
        "last_name",
        "is_admin",
        "is_superuser",
    ]
    list_filter = ["is_admin"]
    search_fields = ["email", "first_name", "last_name"]
    ordering = ["first_name", "last_name"]
    filter_horizontal = ["groups", "user_permissions"]
    readonly_fields = ["last_login"]
    fieldsets = (
        ("Authentication", {
            "fields": (
                "phone_number",
                "password",
            )
        }),
        (("Personal Info"), {
            "fields": (
                "first_name",
                "last_name",
                "email",
            )
        }),
        (("Permissions"), {
            "fields": (
                "is_active",
                "is_admin",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        (("Important dates"), {
            "fields": ("last_login", )
        }),
    )
    add_fieldsets = (("Create User", {
        "fields": (
            "first_name",
            "last_name",
            "phone_number",
            "email",
            "password1",
            "password2",
        )
    }), )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        if not is_superuser:
            form.base_fields["is_superuser"].disabled = True
        return form


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ["otp", "phone_number", "created_at"]
