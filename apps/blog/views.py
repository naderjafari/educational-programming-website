from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import FormMixin

from .models import Post, Category, Comment, Favorite
from .forms import CommentForm
from ..subscriptions.utils import user_has_active_subscription


class HomeView(ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = "posts"
    paginate_by = 10
    ordering = ["-created_at"]


class CategoryListView(ListView):
    model = Post
    template_name = "blog/category_list.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs["category_id"])
        return Post.objects.filter(categories=self.category).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        return context


class PostDetailView(FormMixin, DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    form_class = CommentForm

    def get_success_url(self):
        return reverse("post_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        context["related_posts"] = self.object.get_related_posts()
        if user.is_authenticated:
            try:
                favorite = Favorite.objects.get(user=user, post=self.object)
            except Favorite.DoesNotExist:
                favorite = None
            context["favorite_post"] = favorite
        else:
            context["favorite_post"] = (
                None  # اگر کاربر وارد نشده باشد، علاقه‌مندی موجود نیست
            )

        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_premium and not user_has_active_subscription(request.user):
            return redirect(reverse("subscriptions:subscription_required"))
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = self.object
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)


class AddCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/add_comment.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, id=self.kwargs["post_id"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("post_detail", kwargs={"pk": self.kwargs["post_id"]})


class ToggleFavoriteView(LoginRequiredMixin, DeleteView):
    model = Favorite

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs["post_id"])
        favorite, created = Favorite.objects.get_or_create(user=request.user, post=post)
        if not created:
            favorite.delete()
        return redirect("post_detail", pk=post.id)


class AddPostView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ["title", "content", "categories", "is_premium", "image"]
    template_name = "blog/add_post.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_staff  # Only staff can add posts
