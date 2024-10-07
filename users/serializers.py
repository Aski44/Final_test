from rest_framework import serializers
from .models import User, Post, Comment

# Сериализатор пользователя
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'phone_number', 'birth_date', 'created_at', 'updated_at']

# Сериализатор поста
class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')  # Поле только для чтения

    class Meta:
        model = Post
        fields = ['id', 'title', 'text', 'image', 'author', 'created_at', 'updated_at']

# Сериализатор комментария
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')  # Поле только для чтения
    post = serializers.ReadOnlyField(source='post.id')

    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'text', 'created_at', 'updated_at']
