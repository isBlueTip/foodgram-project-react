from djangoHexadecimal.fields import HexadecimalField
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.db import models


User = get_user_model()


class Tag(models.Model):
    BREAKFAST = 'BR'
    DINNER = 'DN'
    SUPPER = 'SP'
    MEAL_TYPE = [
        (BREAKFAST, 'Breakfast'),
        (DINNER, 'Dinner '),
        (SUPPER, 'Supper'),
    ]
    name = models.CharField(
        max_length=2,
        choices=MEAL_TYPE,
        verbose_name='Название тега',
    )
    hex_color = HexadecimalField(
        max_length='8',
        verbose_name='Цвет в HEX-кодировке',
    )


class Recipe(models.Model):
    BREAKFAST = 'BR'
    DINNER = 'DN'
    SUPPER = 'SP'
    MEAL_TYPE = [
        (BREAKFAST, 'Breakfast'),
        (DINNER, 'Dinner '),
        (SUPPER, 'Supper'),
    ]
    name = models.TextField(
        max_length=100,
        verbose_name='Название блюда'
    )
    author = models.ForeignKey(
        User,
        related_name='recipe',
        on_delete=models.PROTECT,
        verbose_name='Автор',
    )
    picture = models.ImageField(
        verbose_name='Фотография готового блюда',
    )
    recipe = models.TextField(
        max_length=500,
        verbose_name='Рецепт',
    )
    ingredients = models.CharField(
        max_length=50,
        verbose_name='Список ингредиентов',
    )
    tag = models.ManyToManyField(
        Tag,
        max_length=10,
        choices=MEAL_TYPE,
        verbose_name='Тип рецепта по времени дня'
    )
    cooking_time = models.PositiveIntegerField(
        validators=[MaxValueValidator(0)],
        max_length=3,
        verbose_name='Время приготовления'
    )


class Ingredient(models.Model):
    name = models.TextField(
        max_length=100,
        verbose_name='Название ингредиента'
    )
    quantity = models.PositiveIntegerField(
        max_length=4,
        verbose_name='Количество',
    )
    units = models.CharField(
        max_length='8',
        verbose_name='Единица измерения',
    )
