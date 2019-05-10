from django.shortcuts import render
from django.http import HttpResponse

from .models import Post, Category, Tag
from config.models import SideBar, Link


def post_list(request, category_id=None, tag_id=None):
    tag = None
    category = None

    if tag_id:
        posts, tag = Post.get_by_tag(tag_id)
    elif category_id:
        posts, category = Post.get_by_category(category_id)
    else:
        posts = Post.latest_posts()

    context = {
        'category': category,
        'tag': tag,
        'post_list': posts,
        'sidebars': SideBar.get_all(),
    }
    context.update(Category.get_navs())

    return render(request, 'blog/list.html', context=context)


def post_detail(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        post = None

    context = {
        'post': post,
        'sidebars': SideBar.get_all(),
    }
    context.update(Category.get_navs())

    return render(request, 'blog/detail.html', context=context)
