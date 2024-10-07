from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import EmailValidator
from .validators import validate_password, validate_email_domain


# Модель пользователя
class User(AbstractUser):
    phone_number = models.CharField(max_length=15)
    birth_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Валидатор для email
    email = models.EmailField(
        validators=[EmailValidator(), validate_email_domain],
        unique=True
    )

    # Указание валидатора для пароля
    password = models.CharField(max_length=128, validators=[validate_password])

def __str__(self):
        return self.username

from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

# Запрещенные слова
FORBIDDEN_WORDS = ['ерунда', 'глупость', 'чепуха']

# Проверка на запрещенные слова в заголовке
def validate_title_no_forbidden_words(value):
    for word in FORBIDDEN_WORDS:
        if word in value.lower():
            raise ValidationError(_('Заголовок не должен содержать запрещенные слова: "%(word)s".') % {'word': word})

# Проверка возраста автора (18+)
def validate_author_age(author):
    if author.birth_date:
        age = (timezone.now().date() - author.birth_date).days // 365
        if age < 18:
            raise ValidationError(_('Автор должен быть старше 18 лет.'))
    else:
        raise ValidationError(_('Дата рождения автора не указана.'))

# Модель поста
class Post(models.Model):
    title = models.CharField(max_length=255, validators=[validate_title_no_forbidden_words])
    text = models.TextField()
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    author = models.ForeignKey('User', on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        # Проверка возраста автора
        validate_author_age(self.author)

    def __str__(self):
        return self.title