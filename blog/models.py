from django.db import models

from accounts.models import User


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField('CREATE AT', auto_now=True)
    updated_at = models.DateTimeField('UPDATED AT', auto_now_add=True)

    class Meta:
        abstract = True


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField('DESCRIPTION', max_length=100, blank=True, help_text='simple one-line text.')

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Post(TimeStampedModel):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
    title = models.CharField('TITLE', max_length=100)
    image = models.ImageField('IMAGE', upload_to='blog/%Y/%m/', blank=True, null=True)
    content = models.TextField('CONTENT')
    like = models.ManyToManyField(User, null=True)
    # slug = models.SlugField('SLUG', max_length=255, unique=True)
    # description = models.CharField('DESCRIPTION', max_length=100, blank=True, help_text='simple description text.')

    def __str__(self):
        return self.title


class Comment(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=50)
    content = models.TextField('content')
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    @property
    def short_content(self):
        return self.content[:10]

    def __str__(self):
        return self.short_content
