from django.db import models
from django.contrib.auth.models import AbstractUser
#from django.core.exceptions import ValidationError


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


class Review(models.Model):
    title_id = models.ForeignKey(
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


class Comments(models.Model):
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

    def __str__(self):
        return self.text
#валидатор - может пригодиться
# def validate_number(value):
#     if value < 1 or value > 10:
#         raise ValidationError('%s some error message' % value)
#     return True

