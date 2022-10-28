from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.db import models

# import base64
# from django.core.files.base import ContentFile


# import csv  # TODO delete for csv import

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=20,
        verbose_name="Название тега",
    )
    color = models.CharField(
        max_length=8,
        # validators=[(),],  # TODO write own HEX validator and delete hexfield from the project
        verbose_name="Цвет в HEX-кодировке",
    )
    slug = (
        models.SlugField(  # TODO auto-fill and check existing slugs (custom validator?)
            max_length=32,
            verbose_name="Slug-адрес",
        )
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название ингредиента")
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name="Единица измерения",
    )

    class Meta:
        ordering = ["-pk"]

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
    name = models.CharField(max_length=200, verbose_name="Название блюда")
    author = models.ForeignKey(
        User,
        related_name="recipe",
        on_delete=models.PROTECT,
        verbose_name="Автор",
    )
    text = models.TextField(
        max_length=3000,
        verbose_name="Рецепт",
    )
    ingredients = models.ManyToManyField(
        Ingredient,  # TODO UniqueConstraint?
        through="IngredientQuantity",
        related_name="recipe",
        verbose_name="Список ингредиентов",
        blank=False,
    )
    cooking_time = models.PositiveIntegerField(
        validators=[MaxValueValidator(360)], verbose_name="Время приготовления"
    )
    image = (
        models.ImageField(  #  TODO string <binary> Картинка, закодированная в Base64
            upload_to="recipes/",
            verbose_name="Фотография готового блюда",
            blank=True,
        )
    )
    tags = models.ManyToManyField(Tag, verbose_name="Теги рецепта")
    pub_date = models.DateTimeField(
        "Дата и время добавления рецепта",
        auto_now_add=True,
    )

    is_in_shopping_cart = models.BooleanField(default=False)

    class Meta:
        ordering = ["-pub_date"]

    def __str__(self):
        return self.name

    def get_tags_list(self):  # TODO return tags list for list_display
        # return Ingredient.objects.get(self)
        # if isinstance(self.ingredients, int):
        return self.tags.all().values_list("name")
        # return 0

    @admin.display(empty_value="unknown")
    def get_ingredients_list(self):
        # return Ingredient.objects.get(self)
        # if isinstance(self.ingredients, int):
        return self.ingredients.all()  # .values_list(flat=True)
        # return 0


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user",
        verbose_name="кто подписался",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="favorite",
        verbose_name="полюбившийся рецепт",
    )

    class Meta:
        verbose_name = "избранное"
        verbose_name_plural = "избранные"


class IngredientQuantity(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(
        validators=[MaxValueValidator(5000)],
        verbose_name="Количество",
        blank=False,
    )

    def __str__(self):
        return f"{self.ingredient}, {self.quantity}"  # TODO add units


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="buyer",
        verbose_name="кто добавил в корзину",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="cart",
        verbose_name="ингредиенты для покупки",
    )

    class Meta:
        verbose_name = "список покупок"
        verbose_name_plural = "списки покупок"
