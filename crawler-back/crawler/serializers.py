from rest_framework import serializers


from .models import Comment, Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'id',
            'url',
            'email',
            'password'
        )


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'id',
            'postUrl',
            'text',
            'author',
        )
