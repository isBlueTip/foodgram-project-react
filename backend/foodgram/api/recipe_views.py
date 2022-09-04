import logging

from api.recipe_serializers import RecipeSerializer, TagSerializer, IngredientSerializer, RecipeFavoriteSerializer
from loggers import formatter, logger
# from .permissions import IsOwnerOrReadOnly
from recipes.models import Recipe, Tag, Ingredient
from rest_framework import viewsets, status, mixins, generics
from rest_framework.response import Response
from api.filters import RecipeFilter, IngredientFilter
from django.forms.models import model_to_dict

from django.shortcuts import get_object_or_404

# from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser#, IsOwnerOrReadOnly



LOG_NAME = 'recipes_views.log'

file_handler = logging.FileHandler(LOG_NAME)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class RecipeViewSet(viewsets.ModelViewSet):
    """Viewset to work with Recipe model."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filterset_class = RecipeFilter
    permission_classes = [IsAuthenticated, ]

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
    pagination_class = None  # TODO why front works only wo/ pagination?


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
        instance = get_object_or_404(Recipe, id=recipe_id)
        user = request.user
        instance.is_favorited.add(user)
        serializer = self.get_serializer(instance=instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        recipe_id = self.kwargs.get('recipe_id')
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        favoritees = recipe.is_favorited
        return favoritees

    def delete(self, request, *args, **kwargs):
        recipe_id = kwargs.get('recipe_id')
        instance = get_object_or_404(Recipe, id=recipe_id)
        user = request.user
        instance.is_favorited.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)
