from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.mixins import CartViewSet, FavoriteViewSet
from api.recipe_views import IngredientViewSet, RecipeViewSet, TagViewSet
from api.users_views import SubscriptionViewSet, UserViewSet

app_name = "api"

router = SimpleRouter()

router.register("ingredients", IngredientViewSet, basename="ingredient")
router.register("recipes", RecipeViewSet, basename="recipe")
router.register(
    r"recipes/(?P<recipe_id>\d+)/favorite",
    FavoriteViewSet, basename="recipefavorite"
)
router.register(
    r"recipes/(?P<recipe_id>\d+)/shopping_cart",
    CartViewSet, basename="cart"
)
router.register("tags", TagViewSet, basename="tag")
router.register(
    r"users/(?P<user_id>\d+)/subscribe",
    SubscriptionViewSet, basename="subscription"
)
router.register("users", UserViewSet, basename="user")


urlpatterns = [
    path("auth/", include("djoser.urls.authtoken")),
    path("", include(router.urls)),
]
