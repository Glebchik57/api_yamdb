from django.contrib.auth.models import AbstractUser
from django.db import models


CHOICES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=20,
        choices=CHOICES,
        default='user',
        blank=True,
        null=True,
    )
    email = models.EmailField(
        unique=True,
    )

    class Meta(AbstractUser.Meta):
        unique_together = ['username', 'email']

    def __str__(self):
        return self.username
