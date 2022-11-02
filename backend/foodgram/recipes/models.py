from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.db import models


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


class Recipe(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название блюда")
    author = models.ForeignKey(
        User,
        related_name="recipes",
        on_delete=models.PROTECT,
        verbose_name="Автор",
    )
    text = models.TextField(
        max_length=3000,
        verbose_name="Рецепт",
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through="IngredientQuantity",
        related_name="recipes",
        verbose_name="Список ингредиентов",
        blank=False,
    )
    cooking_time = models.PositiveIntegerField(
        validators=[MaxValueValidator(360)], verbose_name="Время приготовления"
    )
    image = models.ImageField(
        upload_to="recipes/",
        verbose_name="Фотография готового блюда",
        blank=True,
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

    def get_tags_list(self):
        return self.tags.all().values_list("name")

    @admin.display(empty_value="unknown")
    def get_ingredients_list(self):
        return self.ingredients.all()


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
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_favorite_recipe',
            )
        ]
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
        return f"{self.ingredient}, {self.quantity}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient',
            )
        ]


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
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_cart',
            )
        ]
        verbose_name = "список покупок"
        verbose_name_plural = "списки покупок"
