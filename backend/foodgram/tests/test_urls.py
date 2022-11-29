import logging
from http import HTTPStatus

from rest_framework import test

from recipes.models import Ingredient, Recipe, Tag
from tests import fixtures
from users.models import User

logger = logging.getLogger("logger")


def test_urls_list(self, urls_list, client, response_code):
    for url in urls_list:
        with self.subTest(url=url):
            response = client.get(url)
            test.APITestCase.assertEqual(self, response.status_code,
                                         response_code)


class URLsTest(test.APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username="HasNoName")
        cls.guest_client = test.APIClient()
        cls.authenticated_client = test.APIClient()
        cls.authenticated_client.force_authenticate(cls.user)
        recipe = Recipe.objects.create(
            name=fixtures.recipe_name,
            author=URLsTest.user,
            cooking_time=fixtures.cooking_time,
        )
        tag = Tag.objects.create(slug=fixtures.tag_1_slug)
        ingredient = Ingredient.objects.create(
            name=fixtures.ingredient_1_name)
        cls.authenticated_urls = fixtures.authenticated_urls + [
            "/api/users/" + str(cls.user.id) + "/",
        ]
        cls.unauthenticated_urls = fixtures.unauthenticated_urls + [
            "/api/tags/" + str(tag.id) + "/",
            "/api/recipes/" + str(recipe.id) + "/",
            "/api/ingredients/" + str(ingredient.id) + "/",
        ]

    def test_urls_for_authenticated(self):
        test_urls_list(
            self,
            fixtures.authenticated_urls,
            URLsTest.authenticated_client,
            HTTPStatus.OK,
        )

        test_urls_list(
            self,
            URLsTest.unauthenticated_urls,
            URLsTest.authenticated_client,
            HTTPStatus.OK,
        )

    def test_urls_for_guest(self):
        test_urls_list(
            self,
            fixtures.authenticated_urls,
            URLsTest.guest_client,
            HTTPStatus.UNAUTHORIZED,
        )

        test_urls_list(
            self,
            URLsTest.unauthenticated_urls,
            URLsTest.guest_client,
            HTTPStatus.OK
        )
