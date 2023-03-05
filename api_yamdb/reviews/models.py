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
        pass

    def __str__(self):
        return self.username

    def user(self):
        return self.role == 'user'

    def moderator(self):
        return self.role == 'moderator'

    def admin(self):
        return self.role == 'admin'
