# Generated by Django 4.0.7 on 2022-08-21 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_alter_user_first_name_alter_user_last_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="confirmation_code",
            field=models.CharField(blank=True, max_length=8),
        ),
    ]