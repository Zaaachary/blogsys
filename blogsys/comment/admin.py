from django.contrib import admin

from .models import Comment
# from blog.models import Post


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('target', 'nickname', 'status', 'created_time')
    fields = (
        'target',
        ('nickname', 'email'),
        'website',
        'content',
    )
