import logging
import traceback

from azbankgateways.exceptions import AZBankGatewaysException
from azbankgateways.models import BankType
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from .models import SubscriptionPlan, Subscription, Payment
from .forms import SubscriptionForm
from azbankgateways import (
    bankfactories,
    models as bank_models,
    default_settings as settings,
)

from decimal import Decimal


class PricingView(ListView):
    model = SubscriptionPlan
    template_name = "subscriptions/pricing.html"
    context_object_name = "plans"


class SubscribeView(LoginRequiredMixin, CreateView):
    model = Subscription
    form_class = SubscriptionForm
    template_name = "subscriptions/subscribe.html"

    def get_initial(self):
        plan_id = self.kwargs.get("pk")
        plan = get_object_or_404(SubscriptionPlan, pk=plan_id)
        return {"plan": plan}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        plan_id = self.kwargs.get("pk")
        context["plan"] = get_object_or_404(SubscriptionPlan, pk=plan_id)
        context["form"].fields["plan"].queryset = SubscriptionPlan.objects.all()
        return context

    def form_valid(self, form):
        user = self.request.user

        # اطلاعات اشتراک فعلی
        active_subscription = Subscription.objects.filter(
            user=user, is_active=True
        ).first()

        if active_subscription:
            form.add_error("plan", "شما یک اشتراک فعال دارید")
            return self.form_invalid(form)

        subscription = form.save(commit=False)

        subscription.user = self.request.user
        subscription.is_active = False  # اشتراک در ابتدا غیرفعال است
        subscription.save()

        amount = int(subscription.plan.price * 10)  # تبدیل به ریال
        factory = bankfactories.BankFactory()
        try:
            bank = factory.create(BankType.PAYV1)
            bank.set_request(self.request)
            bank.set_amount(amount)
            # ارسال شناسه اشتراک به عنوان reference_number
            bank.set_client_callback_url(
                self.request.build_absolute_uri(
                    reverse("subscriptions:callback-gateway")
                    + f"?subscription_id={subscription.id}"
                )
            )
            bank_record = bank.ready()
            return bank.redirect_gateway()
        except AZBankGatewaysException as e:
            logging.error(f"خطا در اتصال به درگاه پرداخت: {str(e)}")
            subscription.delete()  # حذف اشتراک در صورت خطا
            return HttpResponse(
                "خطا در اتصال به درگاه پرداخت. لطفاً بعداً دوباره امتحان کنید."
            )


class SubscriptionSuccessView(LoginRequiredMixin, TemplateView):
    template_name = "subscriptions/success.html"


class SubscriptionFailedView(TemplateView):
    template_name = "subscriptions/failed.html"


class SubscriptionRequiredView(TemplateView):
    template_name = "subscriptions/required.html"


class CallbackGatewayView(View):
    def get(self, request, *args, **kwargs):
        tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
        subscription_id = request.GET.get("subscription_id", None)

        if not tracking_code or not subscription_id:
            logging.error("No tracking code or subscription ID available")
            return redirect("subscriptions:subscription_failed")

        try:
            bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
            subscription = get_object_or_404(Subscription, id=subscription_id)
        except bank_models.Bank.DoesNotExist:
            logging.error("Bank record does not exist")
            return redirect("subscriptions:subscription_failed")

        amount = Decimal(bank_record.amount) / Decimal("10")

        if bank_record.is_success:
            Payment.objects.create(
                user=subscription.user,
                subscription=subscription,
                amount=amount,
                transaction_id=bank_record.tracking_code,
                status="completed",
            )
            subscription.is_active = True
            subscription.start_date = timezone.now()
            subscription.end_date = subscription.start_date + timezone.timedelta(
                days=subscription.plan.duration_days
            )
            subscription.save()
            return redirect("subscriptions:subscription_success")
        else:
            Payment.objects.create(
                user=subscription.user,
                subscription=subscription,
                amount=bank_record.amount,
                transaction_id=bank_record.tracking_code,
                status="failed",
            )
            subscription.delete()  # حذف اشتراک ناموفق
            return redirect("subscriptions:subscription_failed")
