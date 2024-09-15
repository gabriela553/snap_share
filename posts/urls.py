from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PostCreateView, PostViewSet

router = DefaultRouter()
router.register(r"posts", PostViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("add/", PostCreateView.as_view(), name="add_post"),
]
