from django.urls import path

from .views import CustomAuthToken, LogoutView, RegisterView, UserListCreate

urlpatterns = [
    path("users/", UserListCreate.as_view(), name="user-list-create"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomAuthToken.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
