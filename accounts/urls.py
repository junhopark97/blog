from django.urls import path, include
from rest_framework import routers

from accounts.views import UserRegisterView, UserLoginView, UserVerifyView

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('verify/', UserVerifyView.as_view(), name='verify'),
]
