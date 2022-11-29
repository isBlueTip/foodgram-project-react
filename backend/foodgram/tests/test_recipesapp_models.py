import logging

from django import test
from django.db.utils import IntegrityError

from recipes.models import (Cart, Favorite, Ingredient, IngredientQuantity,
                            Recipe, Tag)
from tests import fixtures
from users.models import USER, User

logger = logging.getLogger("logger")


class RecipeFixtures(test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_1 = User.objects.create(
            first_name=fixtures.user_2_first_name,
            last_name=fixtures.user_2_last_name,
            email=fixtures.user_2_email,
            role=USER,
        )
        cls.tag_1 = Tag.objects.create(
            name=fixtures.tag_1_name,
            color=fixtures.tag_1_color,
            slug=fixtures.tag_1_slug,
        )
        cls.tag_2 = Tag.objects.create(
            name=fixtures.tag_2_name,
            color=fixtures.tag_2_color,
            slug=fixtures.tag_2_slug,
        )
        cls.ingredient_1 = Ingredient.objects.create(
            name=fixtures.ingredient_1_name,
            measurement_unit=fixtures.measurement_unit_1,
        )
        cls.ingredient_2 = Ingredient.objects.create(
            name=fixtures.ingredient_2_name,
            measurement_unit=fixtures.measurement_unit_2,
        )
        cls.recipe_1 = Recipe.objects.create(
            name=fixtures.recipe_name,
            author=cls.user_1,
            text=fixtures.recipe_description,
            cooking_time=fixtures.cooking_time,
            # image=,
            is_in_shopping_cart=True,
        )
        cls.ingredient_quantity_1 = IngredientQuantity.objects.create(
            recipe=cls.recipe_1,
            ingredient=cls.ingredient_1,
            quantity=fixtures.quantity_1,
        )
        cls.ingredient_quantity_2 = IngredientQuantity.objects.create(
            recipe=cls.recipe_1,
            ingredient=cls.ingredient_2,
            quantity=fixtures.quantity_2,
        )

        cls.recipe_1.tags.set([cls.tag_1, cls.tag_2])


class TagModelTest(RecipeFixtures):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_object_fields(self):
        expected_values = {
            "name": fixtures.tag_1_name,
            "color": fixtures.tag_1_color,
            "slug": fixtures.tag_1_slug,
        }
        for field, expected_value in expected_values.items():
            with self.subTest(field=field):
                self.assertEqual(getattr(TagModelTest.tag_1, field),
                                 expected_value)


class IngredientModelTest(RecipeFixtures):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_object_fields(self):
        expected_values = {
            "name": fixtures.ingredient_1_name,
            "measurement_unit": fixtures.measurement_unit_1,
        }
        for field, expected_value in expected_values.items():
            with self.subTest(field=field):
                self.assertEqual(
                    getattr(IngredientModelTest.ingredient_1, field),
                    expected_value
                )


class RecipeModelTest(RecipeFixtures):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_object_fields(self):
        expected_values = {
            "name": fixtures.recipe_name,
            "author": RecipeModelTest.user_1,
            "text": fixtures.recipe_description,
            "cooking_time": fixtures.cooking_time,
            "is_in_shopping_cart": True,
        }
        m2m_values = {
            "tags": [RecipeModelTest.tag_1, RecipeModelTest.tag_2],
            "ingredients": [
                RecipeModelTest.ingredient_quantity_1,
                RecipeModelTest.ingredient_quantity_2,
            ],
        }
        for field, expected_value in expected_values.items():
            with self.subTest(field=field):
                self.assertEqual(
                    getattr(RecipeModelTest.recipe_1, field), expected_value
                )

        self.assertEqual(
            list(Tag.objects.filter(recipe=RecipeModelTest.recipe_1)),
            m2m_values.get("tags"),
        )
        self.assertEqual(
            list(IngredientQuantity.objects.filter(
                recipe=RecipeModelTest.recipe_1)
            ),
            m2m_values.get("ingredients"),
        )


class FavoriteModelTest(RecipeFixtures):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.favorite_1 = Favorite.objects.create(
            user=FavoriteModelTest.user_1,
            recipe=FavoriteModelTest.recipe_1,
        )

    def test_object_fields(self):
        expected_values = {
            "user": FavoriteModelTest.user_1,
            "recipe": FavoriteModelTest.recipe_1,
        }
        for field, expected_value in expected_values.items():
            with self.subTest(field=field):
                self.assertEqual(
                    getattr(FavoriteModelTest.favorite_1, field),
                    expected_value
                )

    def test_unique_favorite(self):
        with self.assertRaises(IntegrityError):
            Favorite.objects.create(
                user=FavoriteModelTest.user_1,
                recipe=FavoriteModelTest.recipe_1,
            )


class IngredientQuantityModelTest(RecipeFixtures):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_object_fields(self):
        expected_values = {
            "recipe": IngredientQuantityModelTest.recipe_1,
            "ingredient": IngredientQuantityModelTest.ingredient_1,
            "quantity": fixtures.quantity_1,
        }
        for field, expected_value in expected_values.items():
            with self.subTest(field=field):
                self.assertEqual(
                    getattr(IngredientQuantityModelTest.ingredient_quantity_1,
                            field),
                    expected_value,
                )

    def test_unique_ingredient_quantity(self):
        with self.assertRaises(IntegrityError):
            IngredientQuantity.objects.create(
                recipe=IngredientQuantityModelTest.recipe_1,
                ingredient=IngredientQuantityModelTest.ingredient_1,
                quantity=fixtures.quantity_1,
            )


class CartModelTest(RecipeFixtures):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.cart_1 = Cart.objects.create(
            user=CartModelTest.user_1,
            recipe=CartModelTest.recipe_1,
        )

    def test_object_fields(self):
        expected_values = {
            "user": CartModelTest.user_1,
            "recipe": CartModelTest.recipe_1,
        }
        for field, expected_value in expected_values.items():
            with self.subTest(field=field):
                self.assertEqual(getattr(CartModelTest.cart_1, field),
                                 expected_value)

    def test_unique_favorite(self):
        with self.assertRaises(IntegrityError):
            Cart.objects.create(
                user=CartModelTest.user_1,
                recipe=CartModelTest.recipe_1,
            )
