# Generated by Django 4.1.1 on 2022-10-28 06:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("recipes", "0019_remove_recipe_is_favorited"),
    ]

    operations = [
        migrations.CreateModel(
            name="Cart",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "recipe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cart",
                        to="recipes.recipe",
                        verbose_name="ингредиенты для покупки",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="buyer",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="кто добавил в корзину",
                    ),
                ),
            ],
            options={
                "verbose_name": "список покупок",
                "verbose_name_plural": "списки покупок",
            },
        ),
    ]
