from django.urls import path
from .views import (
    HomeView,
    CategoryListView,
    PostDetailView,
    AddCommentView,
    ToggleFavoriteView,
    AddPostView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path(
        "category/<int:category_id>/", CategoryListView.as_view(), name="category_list"
    ),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("post/<int:post_id>/comment/", AddCommentView.as_view(), name="add_comment"),
    path(
        "post/<int:post_id>/favorite/",
        ToggleFavoriteView.as_view(),
        name="toggle_favorite",
    ),
    path("add-post/", AddPostView.as_view(), name="add_post"),
]
