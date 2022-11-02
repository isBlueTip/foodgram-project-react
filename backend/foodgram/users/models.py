from django.contrib.auth.models import AbstractUser
from django.db import models

ADMIN = "admin"
USER = "user"


class User(AbstractUser):
    USER_ROLES = [
        (USER, "User"),
        (ADMIN, "Admin"),
    ]
    first_name = models.CharField(
        "first name",
        max_length=150,
        blank=False,
    )
    last_name = models.CharField(
        "last name",
        max_length=150,
        blank=False,
    )
    email = models.EmailField(
        "email address",
        unique=True,
        blank=False,
        null=False,
    )
    role = models.CharField(
        "роль на сайте", max_length=32, choices=USER_ROLES, default=USER
    )

    class Meta:
        ordering = ["-id"]
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __str__(self):
        if self.get_full_name():
            return self.get_full_name()
        return self.username


class Subscription(models.Model):
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name="кто подписался",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscription",
        verbose_name="на кого подписка",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['follower', 'author'],
                name='unique_subscription',
            )
        ]
        verbose_name = "избранное"
        verbose_name_plural = "избранные"
