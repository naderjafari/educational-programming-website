from django.contrib import admin
from .models import SubscriptionPlan, Subscription, Payment


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "duration_days")
    list_filter = ("duration_days",)
    search_fields = ("name",)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "plan", "start_date", "end_date", "is_active")
    list_filter = ("is_active", "plan")
    search_fields = ("user__username", "user__email")
    date_hierarchy = "start_date"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("user", "plan")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("user", "subscription", "amount", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("user__username", "user__email", "transaction_id")
    date_hierarchy = "created_at"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("user", "subscription")
