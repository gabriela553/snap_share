from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Post

HTTP_OK = 200


class PostsListTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.post1 = Post.objects.create(image="\\posts\\media\\image1.png", caption="The content of the first post", author=self.user)
        self.post2 = Post.objects.create(image="\\posts\\media\\image2.jpg", caption="The content of the second post", author=self.user)

    def test_post_list(self):
        response = self.client.get(reverse("post_list"))
        response_data = response.json()
        posts = response_data["posts"]
        self.assertEqual(response.status_code, HTTP_OK)
        self.assertEqual(len(posts), 2)
        self.assertEqual(posts[0]["caption"], self.post1.caption)
        self.assertEqual(posts[1]["caption"], self.post2.caption)
