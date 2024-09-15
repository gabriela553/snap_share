from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CommentCreateView,
    LikeCreateView,
    PostCreateView,
    PostViewSet,
)

router = DefaultRouter()
router.register(r"posts", PostViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("add/", PostCreateView.as_view(), name="add_post"),
    path("comments/", CommentCreateView.as_view(), name="create_comment"),
    path("likes/", LikeCreateView.as_view(), name="like_create"),
]
