from django.contrib import admin
from django.utils.html import format_html
from .models import Post, User  # Import only once


# Настраиваем админ-панель для модели Post
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Отображаемые поля в списке постов
    list_display = ['title', 'author_link', 'created_at', 'updated_at']
    # Добавление фильтра по дате создания поста
    list_filter = ['created_at']
    # Добавляем поле поиска
    search_fields = ['title', 'author__username']

    # Метод для создания ссылки на автора
    def author_link(self, obj):
        return format_html('<a href="/admin/blog_app/user/{}/change/">{}</a>', obj.author.id, obj.author.username)

    # Переименовываем колонку
    author_link.short_description = 'Автор'
    author_link.admin_order_field = 'author'
    author_link.empty_value_display = '-'  # Adding in the combined version for completeness


# Регистрируем модели
admin.site.register(User)
