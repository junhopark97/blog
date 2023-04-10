from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from accounts.serializers import UserRegisterSerializer, UserLoginSerializer, UserVerifySerializer


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny,)


class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # print(serializer.__dict__)

        token = serializer.validated_data
        res = Response(
            {
                'token': token,
                'message': 'Login success',
            },
            status=status.HTTP_200_OK,
        )
        res.set_cookie(
            key='jwt',
            value=token,
            httponly=True,
        )

        return res


class UserVerifyView(generics.GenericAPIView):
    serializer_class = UserVerifySerializer
    permission_classes = (AllowAny,)

    def get(self, request):
        serializer = self.get_serializer(data=request)
        data = serializer.to_internal_value(request)

        if 'access_token' in data:
            # access 토큰 갱신.
            res = Response(
                {
                    'token': data,
                    'message': 'Access token renewal successful',
                },
                status=status.HTTP_200_OK,
            )
            res.set_cookie(
                key='jwt',
                value=data,
                httponly=True,
            )
            return res

        return Response(data)

