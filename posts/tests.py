from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Post

HTTP_OK = 200


class PostsListTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
        )
        self.client.force_authenticate(user=self.user)
        self.post1 = Post.objects.create(
            image="\\media\\posts\\test_image1.png",
            caption="The content of the first post",
            author=self.user,
        )
        self.post2 = Post.objects.create(
            image="\\media\\posts\\test_image2.jpg",
            caption="The content of the second post",
            author=self.user,
        )

    def test_post_list(self):
        response = self.client.get("/api/posts/")
        response_data = response.json()

        self.assertEqual(response.status_code, HTTP_OK)
        self.assertEqual(len(response_data), 2)
        self.assertEqual(response_data[0]["caption"], self.post2.caption)
        self.assertEqual(response_data[1]["caption"], self.post1.caption)
