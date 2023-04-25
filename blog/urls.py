from django.urls import path, include
from rest_framework import routers

# from blog.views import PostListView, PostDetailView, like_post
from blog.views import like_post, PostViewSet

post_router = routers.SimpleRouter()
post_router.register('posts', PostViewSet)
# post_router = routers.DefaultRouter()
# post_router.register('post', viewset=PostViewSet, basename='post')

urlpatterns = [
    path('', include(post_router.urls)),
    # path('posts/', PostListView.as_view(), name='post-list'),
    # path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/like/<int:pk>/', like_post, name='like-post'),
]
