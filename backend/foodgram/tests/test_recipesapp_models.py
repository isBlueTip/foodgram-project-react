from django import test
from django.db.utils import IntegrityError

from users.models import Subscription, User, ADMIN, USER
from recipes.models import Tag, Ingredient, Recipe, IngredientQuantity, Favorite, Cart
from tests import fixtures


class RecipeFixtures(test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # cls.user_1 = User.objects.create(
        #     first_name=fixtures.user_1_first_name,
        #     last_name=fixtures.user_1_last_name,
        #     username=fixtures.user_1_username,
        #     email=fixtures.user_1_email,
        #     role=USER,
        # )
        cls.user_1 = User.objects.create(
            first_name=fixtures.user_2_first_name,
            last_name=fixtures.user_2_last_name,
            email=fixtures.user_2_email,
            role=ADMIN,
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


class TagModelTest(RecipeFixtures):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_object_fields(self):
        expected_values = {
            'name': fixtures.tag_1_name,
            'color': fixtures.tag_1_color,
            'slug': fixtures.tag_1_slug,
        }
        for field, expected_value in expected_values.items():
            with self.subTest(field=field):
                self.assertEqual(
                    getattr(TagModelTest.tag_1, field), expected_value)


class IngredientModelTest(RecipeFixtures):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_object_fields(self):
        expected_values = {
            'name': fixtures.ingredient_1_name,
            'measurement_unit': fixtures.measurement_unit_1,
        }
        for field, expected_value in expected_values.items():
            with self.subTest(field=field):
                self.assertEqual(
                    getattr(IngredientModelTest.ingredient_1,
                            field), expected_value)
