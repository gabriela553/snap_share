from rest_framework import status, viewsets
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Comment, Like, Post
from .serializers import CommentSerializer, LikeSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = (
        Post.objects.all()
        .order_by("-created_at")
        .select_related("author")
        .prefetch_related("likes", "comments")
    )
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentCreateView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class LikeCreateView(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_clas = LikeSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        post_id = request.data.get("post")
        if not post_id:
            return Response(
                {"detail": "Post ID is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response(
                {"detail": "Post not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if Like.objects.filter(post=post, user=request.user).exists():
            return Response(
                {"detail": "You have already liked this post."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        like = Like.objects.create(post=post, user=request.user)
        serializer = LikeSerializer(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
