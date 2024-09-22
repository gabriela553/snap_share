from django.urls import path

from .views import RegisterView, UserListCreate

urlpatterns = [
    path("users/", UserListCreate.as_view(), name="user-list-create"),
    path("register/", RegisterView.as_view(), name="register"),
]
