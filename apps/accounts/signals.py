from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # اگر نیاز به ایجاد پروفایل یا انجام کار دیگری پس از ایجاد کاربر دارید، اینجا انجام دهید
        pass


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    # اگر نیاز به انجام کاری پس از ذخیره کاربر دارید، اینجا انجام دهید
    pass
