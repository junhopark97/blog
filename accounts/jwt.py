from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):  # noqa
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['user_id'] = str(user.id)
        token['email'] = user.email

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data["user_id"] = str(user.id)
        data["email"] = user.email
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
