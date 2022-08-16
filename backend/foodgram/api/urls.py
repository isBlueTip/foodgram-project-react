from django.urls import include, path

from rest_framework.routers import SimpleRouter
# from rest_framework.authtoken import views

from api.recipes_views import RecipeViewSet, TagViewSet

router = SimpleRouter()

router.register('recipes', RecipeViewSet)
router.register('tags', TagViewSet)
# router.register(
#     r'posts/(?P<post_id>\d+)/comments',
#     CommentViewSet, basename='comment'
# )


api_patterns = [
    # path('', include(router.urls)),
    path('', include(router.urls)),
    # path('v1/api-token-auth/', views.obtain_auth_token),
]

urlpatterns = [
    path('', include(api_patterns)),
]
