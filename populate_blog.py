import os
import sys
import django
import random
from faker import Faker
import requests
from io import BytesIO
from django.core.files import File
from phonenumber_field.phonenumber import PhoneNumber

# تنظیم محیط Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model
from apps.blog.models import Post, Comment

User = get_user_model()
fake = Faker("fa_IR")

# لیست نام‌های فارسی
persian_names = [
    "علی",
    "محمد",
    "فاطمه",
    "زهرا",
    "حسین",
    "حسن",
    "مریم",
    "سارا",
    "رضا",
    "امیر",
    "نرگس",
    "زینب",
    "احمد",
    "محسن",
    "لیلا",
    "مهدی",
    "فرزانه",
    "امید",
    "ندا",
    "سعید",
    "الهام",
    "مجید",
    "شیما",
    "پریسا",
    "حمید",
    "نازنین",
    "بهروز",
    "مینا",
    "کاوه",
    "نیلوفر",
]

# لیست جملات کوتاه فارسی برای نظرات
persian_comments = [
    "مطلب بسیار جالبی بود، ممنون.",
    "کاش توضیحات بیشتری می‌دادید.",
    "این مقاله به من خیلی کمک کرد.",
    "نکات خوبی داشت، منتظر مطالب بعدی هستم.",
    "سوالی که داشتم رو جواب داد، متشکرم.",
    "به نظرم این موضوع نیاز به بررسی بیشتری داره.",
    "خیلی خوب توضیح دادید، ممنون از شما.",
    "امیدوارم در این زمینه مطالب بیشتری منتشر کنید.",
    "نکات کاربردی زیادی داشت.",
    "با بخش‌هایی از مقاله موافق نیستم، ولی در کل خوب بود.",
]


def create_users(num_users=5):
    users = []
    for _ in range(num_users):
        first_name = random.choice(persian_names)
        last_name = random.choice(persian_names)
        username = fake.user_name()
        email = fake.email()
        password = "password123"  # در یک محیط واقعی، از پسوردهای امن‌تر استفاده کنید
        phone_number = PhoneNumber.from_string(fake.phone_number(), region="IR")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
        )
        users.append(user)
    return users


def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BytesIO(response.content)
    return None


def create_posts(num_posts=20):
    users = create_users()
    for _ in range(num_posts):
        title = fake.sentence()
        content = fake.paragraphs(nb=5)
        content = "\n\n".join(content)
        author = random.choice(users)
        is_premium = random.choice([True, False])

        post = Post(title=title, content=content, author=author, is_premium=is_premium)

        # اضافه کردن تصویر
        image_url = f"https://picsum.photos/800/600"
        image_content = download_image(image_url)
        if image_content:
            post.image.save(f"post_image_{_}.jpg", File(image_content), save=False)

        post.save()

        # ایجاد نظرات
        num_comments = random.randint(0, 5)
        for _ in range(num_comments):
            Comment.objects.create(
                post=post,
                author=random.choice(users),
                content=random.choice(persian_comments),
            )


if __name__ == "__main__":
    print("شروع ایجاد پست‌های وبلاگ...")
    create_posts()
    print("پست‌های وبلاگ با موفقیت ایجاد شدند.")
