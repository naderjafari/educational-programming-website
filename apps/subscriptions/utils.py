from django.utils import timezone


def user_has_active_subscription(user):
    if not user.is_authenticated:
        return False
    return user.subscriptions.filter(
        is_active=True, end_date__gt=timezone.now()
    ).exists()
