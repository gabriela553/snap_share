import time
from pathlib import Path

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from .models import Comment, Like, Post, Tag

User = get_user_model()


class PostsListTests(TestCase):
    TEST_PASSWORD = "testpassword"

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            password=self.TEST_PASSWORD,
        )

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)

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

    def tearDown(self) -> None:
        Post.objects.all().delete()
        User.objects.all().delete()

    def test_post_list(self) -> None:
        response = self.client.get("/api/posts/")
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data["results"]), 2)
        self.assertEqual(response_data["results"][0]["caption"], self.post2.caption)
        self.assertEqual(response_data["results"][1]["caption"], self.post1.caption)


class PostCreateViewTest(APITestCase):
    TEST_PASSWORD = "testpassword"

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="testuser",
            password=self.TEST_PASSWORD,
        )
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)
        self.url = "/api/posts/"

    def tearDown(self) -> None:
        Post.objects.all().delete()
        User.objects.all().delete()

    def test_create_post_authenticated(self) -> None:
        img_path = Path("media/posts/test_image1.png")
        with img_path.open("rb") as img_file:
            data = {"caption": "Test post authenticated", "image": img_file}
            response = self.client.post(self.url, data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().caption, "Test post authenticated")

    def test_create_post_unauthenticated(self) -> None:
        self.client.credentials()
        img_path = Path("media/posts/test_image1.png")
        with img_path.open("rb") as img_file:
            data = {"caption": "Test post authenticated", "image": img_file}
            response = self.client.post(self.url, data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Post.objects.count(), 0)

    def test_create_post_with_tags(self) -> None:
        img_path = Path("media/posts/test_image1.png")
        with img_path.open("rb") as img_file:
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
    TEST_PASSWOED = "testpassword"

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="testuser",
            password=self.TEST_PASSWOED,
        )
        self.post = Post.objects.create(
            image="\\posts\\test_image1.png",
            caption="The content of the first post",
            author=self.user,
        )
        self.url = "/api/comments/"

    def tearDown(self) -> None:
        self.post.delete()
        self.user.delete()

    def test_create_comment_authenticated(self) -> None:
        self.token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        data = {
            "post": self.post.id,
            "content": "This is a test comment.",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.get().content, "This is a test comment.")
        self.assertEqual(Comment.objects.get().author, self.user)

    def test_create_comment_unauthenticated(self) -> None:
        data = {
            "post": self.post.id,
            "content": "This is a test comment.",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Comment.objects.count(), 0)


class LikeCreateViewTest(APITestCase):
    TEST_PASSWORD = "testpassword"

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="testuser",
            password=self.TEST_PASSWORD,
        )
        self.token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.post = Post.objects.create(
            image="\\posts\\test_image1.png",
            caption="The content of the first post",
            author=self.user,
        )
        self.url = "/api/likes/"

    def tearDown(self) -> None:
        self.post.delete()
        self.user.delete()

    def test_create_like_authenticated(self) -> None:
        self.client.force_authenticate(user=self.user)
        data = {
            "post": self.post.id,
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), 1)
        self.assertEqual(Like.objects.get().post, self.post)
        self.assertEqual(Like.objects.get().user, self.user)

    def test_create_like_already_exists(self) -> None:
        self.client.force_authenticate(user=self.user)
        Like.objects.create(post=self.post, user=self.user)
        data = {
            "post": self.post.id,
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "You have already liked this post.")
        self.assertEqual(Like.objects.count(), 1)

    def test_create_like_unauthenticated(self) -> None:
        self.client.credentials()
        data = {
            "post": self.post.id,
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Like.objects.count(), 0)
