from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CommentCreateView,
    LikeCreateView,
    PostViewSet,
)

router = DefaultRouter()
router.register(r"posts", PostViewSet)
router.register(r"comments", CommentCreateView)
router.register(r"likes", LikeCreateView)

urlpatterns = [
    path("", include(router.urls)),
]
