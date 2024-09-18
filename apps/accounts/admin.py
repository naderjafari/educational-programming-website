from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, PhoneVerification
from .forms import CustomUserCreationForm, CustomUserChangeForm


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = (
        "username",
        "email",
        "phone_number",
        "is_phone_verified",
        "subscription_end_date",
        "is_staff",
    )
    list_filter = (
        "is_phone_verified",
        "subscription_end_date",
        "is_staff",
        "is_superuser",
    )
    fieldsets = UserAdmin.fieldsets + (
        (
            "اطلاعات اضافی",
            {"fields": ("phone_number", "is_phone_verified", "subscription_end_date")},
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("اطلاعات اضافی", {"fields": ("phone_number",)}),
    )
    search_fields = ("username", "email", "phone_number")
    ordering = ("username",)


@admin.register(PhoneVerification)
class PhoneVerificationAdmin(admin.ModelAdmin):
    list_display = ("user", "code", "created_at", "expires_at")
    search_fields = ("user__username", "user__phone_number", "code")
