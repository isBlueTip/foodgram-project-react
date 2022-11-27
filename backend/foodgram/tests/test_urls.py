import logging

from rest_framework import test

from tests import fixtures
from users.models import User
from recipes.models import Recipe, Tag, Ingredient
from loggers import formatter, logger_tests

LOG_NAME = "logs/logger_tests.log"

file_handler = logging.FileHandler(LOG_NAME)
file_handler.setFormatter(formatter)
logger_tests.addHandler(file_handler)


class URLsTest(test.APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='HasNoName')
        cls.guest_client = test.APIClient()
        cls.authenticated_client = test.APIClient()
        cls.authenticated_client.force_authenticate(cls.user)
        recipe = Recipe.objects.create(name=fixtures.recipe_name,
                                       author=URLsTest.user,
                                       cooking_time=fixtures.cooking_time)
        tag = Tag.objects.create(slug=fixtures.tag_slug)
        ingredient = Ingredient.objects.create(name=fixtures.ingredient_name)
        cls.authenticated_urls = fixtures.authenticated_urls + [
            '/api/users/' + str(cls.user.id) + '/',
        ]
        cls.unauthenticated_urls = fixtures.unauthenticated_urls + [
            '/api/tags/' + str(tag.id) + '/',
            '/api/recipes/' + str(recipe.id) + '/',
            '/api/ingredients/' + str(ingredient.id) + '/',
        ]

    def test_urls_for_authenticated(self):
        for url in fixtures.authenticated_urls:
            with self.subTest(url=url):
                response = URLsTest.authenticated_client.get(url)
                self.assertEqual(response.status_code, 200)

        for url in URLsTest.unauthenticated_urls:
            with self.subTest(url=url):
                response = URLsTest.authenticated_client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_urls_for_guest(self):
        for url in fixtures.authenticated_urls:
            with self.subTest(url=url):
                response = URLsTest.guest_client.get(url)
                self.assertEqual(response.status_code, 401)

        for url in URLsTest.unauthenticated_urls:
            with self.subTest(url=url):
                response = URLsTest.guest_client.get(url)
                self.assertEqual(response.status_code, 200)
