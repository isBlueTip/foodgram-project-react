import logging

from rest_framework.decorators import action

from api.recipe_serializers import RecipeSerializer, TagSerializer, IngredientSerializer, CartFavoriteSerializer
from loggers import formatter, logger_recipe_views
from recipes.models import Recipe, Tag, Ingredient, Favorite, Cart, IngredientQuantity
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from api.filters import RecipeFilter, IngredientFilter

from django.http import HttpResponse

from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated, AllowAny

from api.permissions import IsAdminOrIsAuthorOrReadOnly


LOG_NAME = 'logs/logger_recipe_views.log'

file_handler = logging.FileHandler(LOG_NAME)
file_handler.setFormatter(formatter)
logger_recipe_views.addHandler(file_handler)


class RecipeViewSet(viewsets.ModelViewSet):
    """Viewset to work with Recipe model."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filterset_class = RecipeFilter
    permission_classes = [IsAdminOrIsAuthorOrReadOnly, ]

    @action(detail=False,
            methods=['get', ],
            permission_classes=[AllowAny, ],
            url_path='download_shopping_cart',)
    def cart(self, request):
        cart = Recipe.objects.filter(cart__user=request.user)
        ingredients = {}
        for recipe in cart:
            ingredient_quantities = IngredientQuantity.objects.filter(recipe=recipe)
            for ingredient in ingredient_quantities.iterator():
                name = ingredient.ingredient.name
                qty = ingredient.quantity
                units = ingredient.ingredient.measurement_unit
                if name in ingredients.keys():
                    ingredients[name][0] += qty
                else:
                    ingredients[name] = [qty, units]

        response = HttpResponse(content_type='text/plain; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="shopping_list.txt"'
        for index, ingredient in enumerate(ingredients):
            response.write(f'{index + 1}. {ingredient}: {ingredients[ingredient][0]} {ingredients[ingredient][1]}\n')
        response.write('Приятного аппетита!')
        return response


class TagViewSet(viewsets.ModelViewSet):
    """Viewset to work with Tag model."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = [AllowAny, ]


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset to work with Ingredient model."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filterset_class = IngredientFilter
    pagination_class = None


class FavoriteViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet,
                      ):
    """Viewset to work with Favorite model."""

    serializer_class = CartFavoriteSerializer
    permission_classes = [IsAuthenticated, ]

    def create(self, request, *args, **kwargs):
        recipe_id = kwargs['recipe_id']
        recipe = get_object_or_404(Recipe, id=recipe_id)
        instance, created = Favorite.objects.get_or_create(
            user=request.user, recipe=recipe,)
        if created:
            serializer = self.get_serializer(instance=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        recipe_id = kwargs.get('recipe_id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        user = request.user
        instance = get_object_or_404(Favorite, user=user, recipe=recipe)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartViewSet(mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet,
                  ):
    """Viewset to work with Cart model."""

    serializer_class = CartFavoriteSerializer
    permission_classes = [IsAuthenticated, ]

    def create(self, request, *args, **kwargs):
        recipe_id = kwargs['recipe_id']
        recipe = get_object_or_404(Recipe, id=recipe_id)
        instance, created = Cart.objects.get_or_create(
            user=request.user, recipe=recipe,)
        if created:
            serializer = self.get_serializer(instance=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        recipe_id = kwargs.get('recipe_id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        user = request.user
        instance = get_object_or_404(Cart, user=user, recipe=recipe)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
