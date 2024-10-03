from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

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
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
