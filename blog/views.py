from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from blog.models import Post
from blog.serializers import PostSerializer


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all().order_by('updated_at')
    pagination_class = PageNumberPagination
