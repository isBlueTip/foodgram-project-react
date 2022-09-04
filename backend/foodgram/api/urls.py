from api.recipe_views import RecipeViewSet, TagViewSet, IngredientViewSet
from api.users_views import UserViewSet
from django.urls import include, path
from rest_framework.routers import SimpleRouter


router = SimpleRouter()

router.register('recipes', RecipeViewSet, basename='recipe')
router.register('tags', TagViewSet, basename='tag')
router.register('users', UserViewSet, basename='user')
router.register('ingredients', IngredientViewSet, basename='ingredient')
# router.register(
#     r'posts/(?P<post_id>\d+)/comments',
#     CommentViewSet, basename='comment'
# )


urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
    # path('auth/', include('djoser.urls')),
]
