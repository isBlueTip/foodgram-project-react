# Generated by Django 4.1.1 on 2022-10-19 08:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0018_favorite"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="recipe",
            name="is_favorited",
        ),
    ]