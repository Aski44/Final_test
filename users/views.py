from rest_framework import viewsets, permissions
from .models import User, Post, Comment
from .serializers import UserSerializer, PostSerializer, CommentSerializer
from .permissions import IsAdminOrSelf, IsAdminOrAuthor, IsAdminOrCommentAuthor

# Представление для пользователей
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['create']:  # Регистрация доступна всем
            return [permissions.AllowAny()]
        elif self.action in ['retrieve', 'list']:  # Просмотр доступен админам и авторизованным пользователям
            return [permissions.IsAuthenticated()]
        elif self.action in ['update', 'partial_update']:  # Редактировать может только админ или сам пользователь
            return [IsAdminOrSelf()]
        elif self.action == 'destroy':  # Удалять может только администратор
            return [permissions.IsAdminUser()]
        return super().get_permissions()

# Представление для постов
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Просмотр для всех

    def get_permissions(self):
        if self.action in ['create']:  # Создавать могут только авторизованные пользователи
            return [permissions.IsAuthenticated()]
        elif self.action in ['update', 'partial_update']:  # Редактировать может админ или автор
            return [IsAdminOrAuthor()]
        elif self.action == 'destroy':  # Удалять может админ или автор
            return [IsAdminOrAuthor()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# Представление для комментариев
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Просмотр для всех

    def get_permissions(self):
        if self.action in ['create']:  # Создавать могут только авторизованные пользователи
            return [permissions.IsAuthenticated()]
        elif self.action in ['update', 'partial_update']:  # Редактировать может админ или автор комментария
            return [IsAdminOrCommentAuthor()]
        elif self.action == 'destroy':  # Удалять может админ или автор комментария
            return [IsAdminOrCommentAuthor()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)# blog_app/views.py
from django.shortcuts import render

posts = [
    {
        'author': 'John Doe',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'October 1, 2024'
    },
]


def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'blog_app/home.html', context)

