from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['user_id'] = str(user.id)
        token['email'] = user.email

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        payload = {
            'user_id': str(user.id),
            'email': user.email,
        }
        token = self.get_token(user)
        token['payload'] = payload
        data.update(token)

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
