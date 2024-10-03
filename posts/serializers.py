from rest_framework import serializers

from .models import Comment, Like, Post, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    tag_names = serializers.ListField(
        child=serializers.CharField(max_length=50),
        required=False,
        write_only=True,
    )

    class Meta:
        model = Post
        fields = ["id", "image", "caption", "created_at", "author", "tags", "tag_names"]
        read_only_fields = ["author"]

    def create(self, validated_data: dict) -> Post:
        tag_names = validated_data.pop("tag_names", [])
        post = Post.objects.create(**validated_data)

        for tag_name in tag_names:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            post.tags.add(tag)

        return post


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "post", "content", "created_at", "author"]
        read_only_fields = ["created_at", "author"]


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["id", "post", "user", "created_at"]
        read_only_fields = ["user", "created_at"]
