from rest_framework import generics, status
from rest_framework.response import Response

from .models import CustomUser
from .serializers import UserRegisterSerializer, UserSerializer


class UserListCreate(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "user": {
                    "username": user.username,
                    "email": user.email,
                },
                "message": "Użytkownik został pomyślnie zarejestrowany.",
            },
            status=status.HTTP_201_CREATED,
        )
