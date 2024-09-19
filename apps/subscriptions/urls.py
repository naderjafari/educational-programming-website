from django.urls import path
from .views import (
    PricingView,
    SubscribeView,
    SubscriptionSuccessView,
    SubscriptionRequiredView,
    CallbackGatewayView,
    SubscriptionFailedView,
)

app_name = "subscriptions"

urlpatterns = [
    path("pricing/", PricingView.as_view(), name="pricing"),
    path("subscribe/<int:pk>/", SubscribeView.as_view(), name="subscribe"),
    path("success/", SubscriptionSuccessView.as_view(), name="subscription_success"),
    path("required/", SubscriptionRequiredView.as_view(), name="subscription_required"),
    path("callback-gateway/", CallbackGatewayView.as_view(), name="callback-gateway"),
    path("failed/", SubscriptionFailedView.as_view(), name="subscription_failed"),
]
