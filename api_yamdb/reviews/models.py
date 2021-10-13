from django.contrib.auth.models import AbstractUser
from django.db import models

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
    role = models.CharField(max_length=300, choices=ROLES, default='user')


class Token(models.Model):
    username = models.CharField(max_length=150)
    confirmation_code = models.CharField(max_length=254)


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=30, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Genre(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=30, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField(null=True, blank=True)
    description = models.TextField(max_length=2000, null=True, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='categories',
    )
    genre = models.ManyToManyField(Genre, blank=True)

    class Meta:
        ordering = ['year']


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title_id', 'author'],
                name='unique_review'
            ),
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    review_id = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['pub_date']

    def __str__(self):
        return self.text
