import json

import pytest
from django.urls import reverse

from accounts.models import User
from blog.models import Post

post_url = reverse('post-list')
pytestmark = pytest.mark.django_db


def test_zero_post_should_return_empty_list(client) -> None:
    response = client.get(post_url)
    assert response.status_code == 200
    assert json.loads(response.content) == []


def test_one_blog_post_exists_should_succeed(client) -> None:
    user = User.objects.create(email='test@example.com', phone_number='1234567890')
    test_blog_post = Post.objects.create(
        title='test',
        slug='blog_post_test',
        description='test',
        author=user,
    )
    response = client.get(post_url)
    response_content = json.loads(response.content)[0]
    author_id = response_content.get('author')
    author = User.objects.get(id=author_id)

    assert response.status_code == 200
    assert response_content.get('title') == test_blog_post.title
    assert response_content.get('slug') == test_blog_post.slug
    assert response_content.get('description') == test_blog_post.description
    assert author.id == test_blog_post.author.id
