from rest_framework import generics

from accounts.models import User
from accounts.serializers import UserRegisterSerializer


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer


# class UserLoginView(generics.GenericAPIView):
#     pass
