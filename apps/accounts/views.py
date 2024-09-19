import logging

import jdatetime
from django.views.generic import CreateView, FormView, TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm, PhoneVerificationForm
from .models import PhoneVerification, CustomUser
import random
import string

from ..blog.models import Favorite
from ..subscriptions.models import Subscription, Payment


class RegisterView(CreateView):
    template_name = "accounts/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("verify_phone")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        code = "".join(random.choices(string.digits, k=6))
        logging.warning(f"Use this code: {code}")
        expires_at = timezone.now() + timezone.timedelta(minutes=10)
        PhoneVerification.objects.create(user=user, code=code, expires_at=expires_at)
        # TODO: Send SMS with code
        return super().form_valid(form)


class VerifyPhoneView(FormView):
    template_name = "accounts/verify_phone.html"
    form_class = PhoneVerificationForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        code = form.cleaned_data["code"]
        verification = PhoneVerification.objects.filter(
            code=code, expires_at__gt=timezone.now(), user__is_active=False
        ).first()

        if verification and code == verification.code:
            user = verification.user
            user.is_active = True
            user.is_phone_verified = True
            user.save()
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error("code", "The verification code is incorrect or expired.")
            return self.form_invalid(form)


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # اطلاعات اشتراک فعلی
        active_subscription = Subscription.objects.filter(
            user=user, is_active=True
        ).first()
        context["active_subscription"] = active_subscription

        # تاریخچه پرداخت‌ها
        payments = Payment.objects.filter(user=user).order_by("-created_at")[:5]
        context["recent_payments"] = payments

        # پست‌های مورد علاقه
        favorite_posts = Favorite.objects.filter(user=user).select_related("post")[:5]
        context["favorite_posts"] = favorite_posts

        return context
