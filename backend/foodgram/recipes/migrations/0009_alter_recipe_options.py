# Generated by Django 4.0.7 on 2022-08-17 04:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0008_rename_units_ingredient_measurement_unit_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="recipe",
            options={"ordering": ["-pub_date"]},
        ),
    ]
