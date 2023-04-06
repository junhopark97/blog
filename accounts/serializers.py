from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.jwt import MyTokenObtainPairSerializer
from accounts.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())],
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password],
    )
    password2 = serializers.CharField(
        write_only=True, required=True,
    )
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'password', 'password2', 'gender', 'username', 'phone_number', 'token')

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

