from users.models import ADMIN, USER
from users.models import User, Subscription
from django.test import TestCase


user_1_first_name = 'H'*12 + 'e'*12 + 'r'*12 + 'oku'
user_1_last_name = 'Dows'
user_1_username = 'John'
user_1_email = 'test@task.com'

user_2_first_name = 'Lucius'
user_2_last_name = 'McLaren'
user_2_email = 'empty@email.com'


tag_slug = 'tag_slug'
ingredient_name = 'test ingredient'
recipe_name = 'test recipe name'
cooking_time = 8


unauthenticated_urls = [
    '/api/tags/',
    '/api/recipes/',
    '/api/ingredients/',
]

authenticated_urls = [
    '/api/users/',
    '/api/users/me/',
    '/api/recipes/download_shopping_cart/',
    '/api/users/subscriptions/',
]

