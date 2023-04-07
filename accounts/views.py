from rest_framework import generics
from rest_framework.permissions import AllowAny

from accounts.models import User
from accounts.serializers import UserRegisterSerializer


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny,)


# class UserLoginView(generics.GenericAPIView):
#     pass
