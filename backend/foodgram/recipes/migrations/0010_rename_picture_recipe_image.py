# Generated by Django 4.0.7 on 2022-08-18 07:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0009_alter_recipe_options"),
    ]

    operations = [
        migrations.RenameField(
            model_name="recipe",
            old_name="picture",
            new_name="image",
        ),
    ]
