import json

import jwt
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from environ import Env
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from accounts.jwt import MyTokenObtainPairSerializer
from accounts.models import User

env = Env()


class UserRegisterSerializer(serializers.ModelSerializer):
    '''
        회원가입
    '''
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())],
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password],
    )
    password2 = serializers.CharField(
        write_only=True, required=True,
    )
    # token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'password', 'password2', 'gender', 'username', 'phone_number')
        # fields = ('email', 'password', 'password2', 'gender', 'username', 'phone_number', 'token')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {'password': "Password fields didn't match."}
            )
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            gender=validated_data['gender'],
            username=validated_data['username'],
            phone_number=validated_data['phone_number'],
        )
        user.save()

        return user

    @classmethod
    def get_token(cls, user):
        token = MyTokenObtainPairSerializer.get_token(user)
        refresh_token = str(token)
        access_token = str(token.access_token)
        return {
            'access': access_token,
            'refresh': refresh_token,
        }


class UserLoginSerializer(serializers.Serializer):  # noqa
    '''
        로그인
    '''
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True, write_only=True,
    )

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )

        try:
            token = MyTokenObtainPairSerializer.get_token(user)
            return {
                'access_token': str(token.access_token),
                'refresh_token': str(token)
            }

        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )


class UserVerifySerializer(serializers.BaseSerializer):  # noqa
    '''
        JWT 토큰 유효성 검증 및 갱신.
    '''
    def to_internal_value(self, data):
        global jwt_dict
        jwt_token = data.COOKIES.get('jwt')
        # json.loads(jwt_token)
        jwt_token = jwt_token.replace("\'", "\"")  # 수정해야 함.

        if not jwt_token:
            return {'message': 'JWT token not found.'}

        try:
            jwt_dict = json.loads(jwt_token)
            access_token = jwt_dict.get('access_token')

            if not access_token:
                return {'message': 'Access token not found in JWT cookie.'}

            # 유저 데이터 확인.
            access_payload = jwt.decode(access_token, env('SECRET_KEY'), algorithms=['HS256'])
            pk = access_payload.get('user_id')
            email = access_payload.get('email')
            try:
                user = get_object_or_404(User, pk=pk, email=email)
            except Http404:
                return {'massage': 'The user information for the access token is invalid.'}

            return {'message': 'JWT token is valid.'}

        except jwt.ExpiredSignatureError:
            # access 토큰 만료시.
            refresh_token = jwt_dict.get('refresh_token', None)

            if not refresh_token:
                return {'message': 'Refresh token not found in JWT cookie.'}

            try:
                refresh_data = {'refresh': refresh_token}
                serializer = TokenRefreshSerializer(data=refresh_data)

                if serializer.is_valid(raise_exception=True):
                    # access 토큰 갱신.
                    new_access_token = serializer.validated_data['access']
                    new_access_payload = jwt.decode(new_access_token, env('SECRET_KEY'), algorithms=['HS256'])
                    pk = new_access_payload.get('user_id')
                    email = new_access_payload.get('email')

                    try:
                        user = get_object_or_404(User, pk=pk, email=email)
                    except Http404:
                        return {'massage': 'The user information for the access token is invalid.'}

                    return {
                        'access_token': str(new_access_token),
                        'refresh_token': str(refresh_token),
                    }

            except (jwt.exceptions.DecodeError, jwt.ExpiredSignatureError):
                # access 토큰, refresh 토큰 만료 시.
                raise serializers.ValidationError('Failed to refresh access token.')
