from django.contrib import admin

from blog.models import Post, Category, Tag, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'tag_list', 'title', 'image', 'like_count', 'created_at', 'updated_at',)

    def tag_list(self, obj):
        return ','.join([t.name for t in obj.tags.all()])

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def like_count(self, obj):
        return obj.likes.count()

    like_count.short_description = 'like'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'author', 'short_content', 'created_at', 'updated_at',)
