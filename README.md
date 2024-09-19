# وبسایت آموزشی برنامه‌نویسی

این پروژه یک وبسایت آموزشی در زمینه برنامه‌نویسی است که با استفاده از Django ایجاد شده است.
کاربران می‌توانند مطالب آموزشی را مشاهده کنند، در دوره‌های پریمیوم ثبت‌نام کنند و نظرات خود را ارسال کنند.

## ویژگی‌ها

- ثبت‌نام و ورود کاربران
- سیستم اشتراک پریمیوم
- مدیریت پست‌های وبلاگ
- سیستم نظردهی
- دسته‌بندی مطالب
- پرداخت آنلاین

## پیش‌نیازها

- Python 3.8+
- Django 4.2+
- PostgreSQL

## نصب و راه‌اندازی

1. مخزن را کلون کنید:
   ```
   git clone https://github.com/naderjafari/educational-programming-website.git
   cd educational-programming-website
   ```

2. یک محیط مجازی ایجاد کنید و آن را فعال کنید:
   ```
   python -m venv venv
   source venv/bin/activate  # در Unix یا MacOS
   # یا
   venv\Scripts\activate  # در Windows
   ```

3. پکیج‌های مورد نیاز را نصب کنید:
   ```
   pip install -r requirements.txt
   ```

4. فایل `.env` را در ریشه پروژه ایجاد کنید و متغیرهای محیطی لازم را تنظیم کنید:
   ```
    # Django settings
    DEBUG=True
      
    # Database settings
    DB_NAME=YOUR_DB_NAME
    DB_USER=postgres
    DB_PASSWORD=YOUR_PASSWORD
    DB_HOST=localhost
    DB_PORT=5432
   ```

5. Migration را اعمال کنید:
   ```
   python manage.py migrate
   ```

6. یک کاربر ادمین ایجاد کنید:
   ```
   python manage.py createsuperuser
   ```

7. سرور توسعه را اجرا کنید:
   ```
   python manage.py runserver
   ```

حالا می‌توانید به آدرس `http://localhost:8000` مراجعه کنید تا وبسایت را مشاهده کنید.

## تکنولوژی‌های استفاده شده

- Django
- PostgreSQL
- Django MPTT
- CKEditor
- Az Iranian Bank Gateways

## مشارکت

اگر می‌خواهید در این پروژه مشارکت کنید، لطفاً ابتدا یک issue ایجاد کنید تا در مورد تغییرات پیشنهادی بحث کنیم. سپس می‌توانید یک Pull Request ارسال کنید.

## مجوز

این پروژه تحت مجوز MIT منتشر شده است. برای جزئیات بیشتر، فایل `LICENSE` را مطالعه کنید.

