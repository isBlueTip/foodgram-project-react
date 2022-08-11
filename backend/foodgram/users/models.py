from django.contrib.auth.models import AbstractUser
from django.db import models

USER = 'user'
ADMIN = 'admin'


class User(AbstractUser):
    USER_ROLES = [
        (USER, 'User'),
        (ADMIN, 'Admin'),
    ]
    # email = models.EmailField(
    #     'email address',
    #     unique=True,
    #     blank=False,
    #     null=False,
    # )
    # bio = models.TextField(
    #     'биография',
    #     blank=True,
    # )
    role = models.CharField(
        'роль на сайте',
        max_length=32,
        choices=USER_ROLES,
        default=USER
    )
    confirmation_code = models.CharField(max_length=8)

    class Meta:
        ordering = ['-id']
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.get_full_name()
