# Generated by Django 4.0.7 on 2022-08-16 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0005_rename_tag_recipe_tags"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipe",
            name="picture",
            field=models.ImageField(
                upload_to="recipes/", verbose_name="Фотография готового блюда"
            ),
        ),
    ]