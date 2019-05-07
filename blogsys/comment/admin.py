from django.contrib import admin

from .models import Comment
from blogsys.custom_site import custom_site     # 自定义site


@admin.register(Comment, site=custom_site)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('target', 'nickname', 'status', 'created_time')
    fields = (
        'target',
        ('nickname', 'email'),
        'website',
        'content',
    )
