# Generated by Django 4.1.1 on 2022-11-02 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0007_subscription_delete_follow"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={
                "ordering": ["-id"],
                "verbose_name": "пользователь",
                "verbose_name_plural": "пользователи",
            },
        ),
        migrations.AddConstraint(
            model_name="subscription",
            constraint=models.UniqueConstraint(
                fields=("follower", "author"), name="unique_subscription"
            ),
        ),
    ]