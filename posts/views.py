from django.shortcuts import redirect, render
from django.http import JsonResponse

from .models import Post


def post_list(request):
    posts = Post.objects.all().order_by("-created_at")
    posts_data = [{"id": post.id, "caption": post.caption, "author": post.author.username} for post in posts]
    return JsonResponse({"posts": posts_data})

