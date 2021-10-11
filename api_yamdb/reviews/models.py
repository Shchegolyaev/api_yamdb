from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

ROLES = (
    ('user', 'Аутентифицированный пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True, blank=False)
    first_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(
        verbose_name='Биография',
        blank=True
    )
    role = models.CharField(max_length=300, choices=ROLES, default=ROLES[0][0])


class Token(models.Model):
    username = models.CharField(max_length=150)
    confirmation_code = models.CharField(max_length=254)
