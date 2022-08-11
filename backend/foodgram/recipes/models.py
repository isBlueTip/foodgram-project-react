# from djangoHexadecimal.fields import HexadecimalField  # TODO delete this package from the project
from django.contrib.auth import get_user_model, admin
from django.contrib import admin
from django.core.validators import MaxValueValidator
from django.db import models


# import csv  # TODO delete for csv import

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        # max_length=2,
        # choices=MEAL_TYPE,
        max_length=20,
        verbose_name='Название тега',
    )
    hex_color = models.CharField(
        max_length=8,
        # validators=[(),],  # TODO write own HEX validator and delete hexfield from the project
        verbose_name='Цвет в HEX-кодировке',
    )
    slug = models.CharField(  # TODO auto-fill and check existing slugs (custom validator?)
        max_length=32,
        verbose_name='Slug-адрес',
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название ингредиента'
    )
    units = models.CharField(
        max_length=12,
        verbose_name='Единица измерения',
    )

    def __str__(self):
        return self.name


#  TODO delete this import
# with open('/home/bluetip/dev/foodgram-project-react/data/ingredients.csv') as f:
#     reader = csv.reader(f)
#     for i, row in enumerate(reader):
#         _, created = Ingredient.objects.get_or_create(
#             id=i + 1,
#             name=row[0],
#             units=row[1],
#         )


class Recipe(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название блюда'
    )
    author = models.ForeignKey(
        User,
        related_name='recipe',
        on_delete=models.PROTECT,
        verbose_name='Автор',
    )
    text = models.TextField(
        max_length=3000,
        verbose_name='Рецепт',
    )
    ingredients = models.ManyToManyField(
        Ingredient,  # TODO UniqueConstraint?
        through='IngredientQuantity',
        related_name='recipe',
        verbose_name='Список ингредиентов',
    )
    cooking_time = models.PositiveIntegerField(
        validators=[MaxValueValidator(360)],
        verbose_name='Время приготовления'
    )
    picture = models.ImageField(
        verbose_name='Фотография готового блюда',
    )
    tag = models.ManyToManyField(
        Tag,
        verbose_name='Теги рецепта'
    )

    def __str__(self):
        return self.name

    def get_tags_list(self):  # TODO return tags list for list_display
        # return Ingredient.objects.get(self)
        # if isinstance(self.ingredients, int):
        return self.tag.all().values_list('name')
        # return 0

    # def get_ingredients_list(self):
    #     # return Ingredient.objects.get(self)
    #     if isinstance(self.ingredients, int):
    #         return self.ingredients
    #     return 0

    @admin.display(empty_value='unknown')
    def get_ingredients_list(self):
        # return Ingredient.objects.get(self)
        # if isinstance(self.ingredients, int):
        return self.ingredients.all()#.values_list(flat=True)
        # return 0


class IngredientQuantity(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(
        validators=[MaxValueValidator(5000)],
        verbose_name='Количество',
    )
