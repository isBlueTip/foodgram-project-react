import logging

from api.recipe_serializers import RecipeSerializer, TagSerializer, IngredientSerializer, RecipeFavoriteSerializer
from loggers import formatter, logger_recipe_views
# from .permissions import IsOwnerOrReadOnly
from recipes.models import Recipe, Tag, Ingredient, Favorite
from rest_framework import viewsets, status, mixins, generics
from rest_framework.response import Response
from api.filters import RecipeFilter, IngredientFilter

from django.shortcuts import get_object_or_404

# from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly

from api.permissions import IsAdminOrIsAuthorOrReadOnly


LOG_NAME = 'logger_recipe_views.log'

file_handler = logging.FileHandler(LOG_NAME)
file_handler.setFormatter(formatter)
logger_recipe_views.addHandler(file_handler)


class RecipeViewSet(viewsets.ModelViewSet):
    """Viewset to work with Recipe model."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filterset_class = RecipeFilter
    permission_classes = [IsAdminOrIsAuthorOrReadOnly, ]

    # def create(self, request, *args, **kwargs):
    #     data = request.data
    #     # logger.debug(data)
    #     serializer = CreateRecipeSerializer(data=data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    #     # return Response(status=status.HTTP_201_CREATED)


class TagViewSet(viewsets.ModelViewSet):
    """Viewset to work with Tag model."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset to work with Recipe model."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filterset_class = IngredientFilter
    pagination_class = None
    # permission_classes = [AllowAny, ]


class RecipeFavoriteViewSet(mixins.CreateModelMixin,
                            mixins.DestroyModelMixin,
                            viewsets.GenericViewSet,
                            ):

    serializer_class = RecipeFavoriteSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        recipe_id = kwargs['recipe_id']
        recipe = get_object_or_404(Recipe, id=recipe_id)
        instance, created = Favorite.objects.get_or_create(
            user=request.user, recipe=recipe,)
        if created:
            serializer = self.get_serializer(instance=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)  # TODO implement custom error message?

    # def get_queryset(self):
    #     recipe_id = self.kwargs.get('recipe_id')
    #     recipe = get_object_or_404(Recipe, pk=recipe_id)
    #     favorite_recipes = recipe.is_favorited
    #     return favorite_recipes

    def delete(self, request, *args, **kwargs):
        recipe_id = kwargs.get('recipe_id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        user = request.user
        instance = get_object_or_404(Favorite, user=user, recipe=recipe)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
