# Generated by Django 4.0.7 on 2022-08-16 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0006_alter_recipe_picture"),
    ]

    operations = [
        migrations.RenameField(
            model_name="tag",
            old_name="hex_color",
            new_name="color",
        ),
    ]
