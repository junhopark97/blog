from django.core.exceptions import ImproperlyConfigured
from rest_framework import generics, status
from rest_framework.exceptions import APIException
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import CustomerAccessPermission
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

        token = serializer.validated_data
        response = Response(
            {
                'token': token,
                'message': 'Login success',
            },
            status=status.HTTP_200_OK,
        )
        response.set_cookie(
            key='jwt',
            value=token,
            httponly=True,
        )

        return response


class UserVerifyView(generics.GenericAPIView):
    serializer_class = UserVerifySerializer
    permission_classes = (CustomerAccessPermission,)

    def get(self, request):
        serializer = self.get_serializer(data=request)
        data = serializer.to_internal_value(request)

        if 'access_token' in data:
            # access 토큰 갱신.
            response = Response(
                {
                    'token': data,
                    'message': 'Access token renewal successful',
                },
                status=status.HTTP_200_OK,
            )
            response.set_cookie(
                key='jwt',
                value=data,
                httponly=True,
            )
            return response

        return Response(data)


class UserLogoutView(APIView):
    permission_classes = (CustomerAccessPermission,)

    def post(self, request):
        try:
            response = Response(
                {
                    'message': 'Logout Successful',
                },
                status=status.HTTP_200_OK,
            )
            response.delete_cookie(key='jwt')

            return response
        except ImproperlyConfigured as e:
            print(e)
            raise APIException('An error occurred during logout')

        except Exception as e:
            print(e)
            raise APIException('An error occurred during logout')
