from django.urls import reverse

user_1_first_name = "H" * 12 + "e" * 12 + "r" * 12 + "oku"
user_1_last_name = "Dows"
user_1_username = "John"
user_1_email = "test@task.com"

user_2_first_name = "Lucius"
user_2_last_name = "McLaren"
user_2_email = "empty@email.com"

tag_1_name = "name"
tag_1_color = "0xe51515"
tag_1_slug = "tag_slug"
tag_2_name = "another tag name"
tag_2_color = "0xa55613"
tag_2_slug = "another_slug"

ingredient_1_name = "test ingredient"
measurement_unit_1 = "г"
quantity_1 = 300
quantity_2 = 550
ingredient_2_name = "another test ingredient"
measurement_unit_2 = "л"

recipe_name = "test recipe name"
recipe_description = "very long description" * 8
cooking_time = 8


tags_url = reverse("api:tag-list")
recipes_url = reverse("api:recipe-list")
ingredients_url = reverse("api:ingredient-list")

unauthenticated_urls = [
    tags_url,
    recipes_url,
    ingredients_url,
]

users_url = reverse("api:user-list")
user_self_info_url = reverse("api:user-me")
download_cart_url = reverse("api:recipe-download_shopping_cart")
subscriptions_url = reverse("api:user-subscriptions")

authenticated_urls = [
    users_url,
    user_self_info_url,
    download_cart_url,
    subscriptions_url,
]
