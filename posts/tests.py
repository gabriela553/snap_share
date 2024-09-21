import time

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from .models import Comment, Like, Post, Tag

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
            image="\\posts\\test_image1.png",
            caption="The content of the first post",
            author=self.user,
        )
        time.sleep(1)
        self.post2 = Post.objects.create(
            image="\\posts\\test_image2.jpg",
            caption="The content of the second post",
            author=self.user,
        )

    def tearDown(self):
        Post.objects.all().delete()
        User.objects.all().delete()

    def test_post_list(self):
        response = self.client.get("/api/posts/")
        response_data = response.json()

        self.assertEqual(response.status_code, HTTP_OK)
        self.assertEqual(len(response_data["results"]), 2)
        self.assertEqual(response_data["results"][0]["caption"], self.post2.caption)
        self.assertEqual(response_data["results"][1]["caption"], self.post1.caption)


class PostCreateViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.url = "/api/add/"

    def tearDown(self):
        Post.objects.all().delete()
        Token.objects.all().delete()
        User.objects.all().delete()

    def test_create_post_authenticated(self):
        self.client.force_authenticate(user=self.user)
        with open("media/posts/test_image1.png", "rb") as img_file:
            data = {"caption": "Test post authenticated", "image": img_file}
            response = self.client.post(self.url, data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().caption, "Test post authenticated")

    def test_create_post_unauthenticated(self):
        self.client.credentials()

        with open("media/posts/test_image1.png", "rb") as img_file:
            data = {"caption": "Test post authenticated", "image": img_file}
            response = self.client.post(self.url, data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Post.objects.count(), 0)

    def test_create_post_with_tags(self):
        self.client.force_authenticate(user=self.user)

        with open("media/posts/test_image1.png", "rb") as img_file:
            data = {
                "caption": "Test post authenticated",
                "image": img_file,
                "tag_names": ["test", "tag"],
            }
            response = self.client.post(self.url, data, format="multipart")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Tag.objects.count(), 2)


class CommentCreateViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
        )
        self.post = Post.objects.create(
            image="\\posts\\test_image1.png",
            caption="The content of the first post",
            author=self.user,
        )
        self.url = "/api/comments/"

    def test_create_comment_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "post": self.post.id,
            "content": "This is a test comment.",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.get().content, "This is a test comment.")
        self.assertEqual(Comment.objects.get().author, self.user)

    def test_create_comment_unauthenticated(self):
        data = {
            "post": self.post.id,
            "content": "This is a test comment.",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Comment.objects.count(), 0)


class LikeCreateViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
        )
        self.post = Post.objects.create(
            image="\\posts\\test_image1.png",
            caption="The content of the first post",
            author=self.user,
        )
        self.url = "/api/likes/"

    def test_create_like_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "post": self.post.id,
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), 1)
        self.assertEqual(Like.objects.get().post, self.post)
        self.assertEqual(Like.objects.get().user, self.user)

    def test_create_like_already_exists(self):
        self.client.force_authenticate(user=self.user)
        Like.objects.create(post=self.post, user=self.user)
        data = {
            "post": self.post.id,
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "You have already liked this post.")
        self.assertEqual(Like.objects.count(), 1)

    def test_create_like_unauthenticated(self):
        data = {
            "post": self.post.id,
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Like.objects.count(), 0)
