from django.urls import path, include
from rest_framework import routers

from blog.views import like_post, PostViewSet, CommentViewSet

router = routers.SimpleRouter()
router.register('posts', PostViewSet)
router.register('comments', CommentViewSet, basename='comments')


urlpatterns = [
    path('', include(router.urls)),
    path('like/<int:pk>/', like_post, name='like-post'),
]
