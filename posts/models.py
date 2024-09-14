from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    image = models.ImageField(upload_to="posts/")
    caption = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    def __str__(self):
        return self.caption
