from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from .validators import validate_year


class User(AbstractUser):
    ROLES = [
        (settings.ROLE_USER, 'Аутентифицированный пользователь'),
        (settings.ROLE_MODERATOR, 'Модератор'),
        (settings.ROLE_ADMIN, 'Администратор'),
    ]
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
        verbose_name='email'
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='имя'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='биография'
    )
    role = models.CharField(
        max_length=300,
        choices=ROLES,
        default='user',
        verbose_name='роль'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Token(models.Model):
    username = models.CharField(
        max_length=150,
        verbose_name='имя пользователя'
    )
    confirmation_code = models.CharField(
        max_length=254,
        verbose_name='код подтверждения'
    )

    class Meta:
        verbose_name = 'Токен'
        verbose_name_plural = 'Токены'


class Category(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='наименование'
    )
    slug = models.SlugField(
        max_length=30,
        unique=True,
        verbose_name='slug'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='наименование'
    )
    slug = models.SlugField(
        max_length=30,
        unique=True,
        verbose_name='slug'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name='наименование'
    )
    year = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), validate_year],
        verbose_name='год'
    )
    description = models.TextField(
        max_length=2000,
        null=True,
        blank=True,
        verbose_name='описание'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='категория'
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        verbose_name='жанр'
    )

    class Meta:
        ordering = ['year']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='произведение'
    )
    text = models.TextField(verbose_name='текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='автор'
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='оценка'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата публикации'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title_id', 'author'],
                name='unique_review'
            ),
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text


class Comment(models.Model):
    review_id = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='отзыв'
    )
    text = models.TextField(verbose_name='текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата публикации'
    )

    class Meta:
        ordering = ['pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
