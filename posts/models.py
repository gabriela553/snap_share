from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    image = models.ImageField(upload_to="posts/")
    caption = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    def __str__(self):
        return self.caption


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f'Comment by {self.author.username} on {self.created_at.strftime
        ("%Y-%m-%d %H:%M:%S")}: {self.content[:50]}'
