from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'username', 'text', 'photo', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'username', 'created_at', 'updated_at']
