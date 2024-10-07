from rest_framework import permissions


# Обобщённый класс разрешений
class IsAdminOrRelatedUser(permissions.BasePermission):
    relation_field = None  # Будет указано в дочерних классах

    def has_object_permission(self, request, view, obj):
        if not hasattr(obj, self.relation_field):
            return False
        related_user = getattr(obj, self.relation_field)
        return request.user.is_staff or related_user == request.user


# Администратор или сам пользователь
class IsAdminOrSelf(IsAdminOrRelatedUser):
    relation_field = 'user'


# Администратор или автор поста
class IsAdminOrAuthor(IsAdminOrRelatedUser):
    relation_field = 'author'


# Администратор или автор комментария
class IsAdminOrCommentAuthor(IsAdminOrRelatedUser):
    relation_field = 'author'