from django.urls import path, include
from rest_framework import routers

from blog.views import PostViewSet

post_router = routers.DefaultRouter()
post_router.register('post', viewset=PostViewSet, basename='post')

# urlpatterns = [
#     # path('', include(post_router.urls)),
# ]
