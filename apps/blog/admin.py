from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category, Post, Comment, Favorite


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    list_display = ("name", "parent")
    search_fields = ("name",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at", "is_premium")
    list_filter = ("is_premium", "created_at", "categories")
    search_fields = ("title", "content")
    filter_horizontal = ("categories",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "post", "created_at")
    list_filter = ("created_at",)
    search_fields = ("content", "author__username", "post__title")


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "post__title")
