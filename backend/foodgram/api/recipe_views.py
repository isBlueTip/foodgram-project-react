import logging

from django.db.models import Sum, Count

from api.filters import IngredientFilter, RecipeFilter
from api.permissions import IsAdminOrIsAuthorOrReadOnly
from api.recipe_serializers import (
    CartFavoriteSerializer,
    IngredientSerializer,
    RecipeSerializer,
    TagSerializer,
)
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from loggers import formatter, logger_recipe_views
from recipes.models import Cart, Favorite, Ingredient, IngredientQuantity, Recipe, Tag
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

LOG_NAME = "logs/logger_recipe_views.log"

file_handler = logging.FileHandler(LOG_NAME)
file_handler.setFormatter(formatter)
logger_recipe_views.addHandler(file_handler)


class RecipeViewSet(viewsets.ModelViewSet):
    """Viewset to work with Recipe model."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filterset_class = RecipeFilter
    permission_classes = [
        IsAdminOrIsAuthorOrReadOnly,
    ]

    @action(
        detail=False,
        methods=[
            "get",
        ],
        permission_classes=[
            AllowAny,
        ],
        url_path="download_shopping_cart",
    )
    def cart(self, request):
        cart = IngredientQuantity.objects.values(
            'ingredient__name',
            'quantity',
            'ingredient__measurement_unit',
        ).order_by('ingredient__id').annotate(total=Sum('ingredient__ingredientquantity__quantity'))
        ingredients = {}
        for ingredient in cart.iterator():
            name = ingredient['ingredient__name']
            if name in ingredients.keys():
                continue
            total = ingredient['total']
            units = ingredient['ingredient__measurement_unit']
            ingredients[name] = [total, units]

        response = HttpResponse(content_type="text/plain; charset=utf-8")
        response["Content-Disposition"] = 'attachment; filename="shopping_list.txt"'
        for index, ingredient in enumerate(ingredients):
            response.write(
                f"{index + 1}. {ingredient}: {ingredients[ingredient][0]} {ingredients[ingredient][1]}\n"
            )
        response.write("Приятного аппетита!")
        return response


class TagViewSet(viewsets.ModelViewSet):
    """Viewset to work with Tag model."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = [
        IsAdminOrIsAuthorOrReadOnly,
    ]


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset to work with Ingredient model."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filterset_class = IngredientFilter
    pagination_class = None


class FavoriteViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Viewset to work with Favorite model."""

    serializer_class = CartFavoriteSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def create(self, request, *args, **kwargs):
        recipe_id = kwargs["recipe_id"]
        recipe = get_object_or_404(Recipe, id=recipe_id)
        instance, created = Favorite.objects.get_or_create(
            user=request.user,
            recipe=recipe,
        )
        if created:
            serializer = self.get_serializer(instance=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        recipe_id = kwargs.get("recipe_id")
        recipe = get_object_or_404(Recipe, id=recipe_id)
        user = request.user
        instance = get_object_or_404(Favorite, user=user, recipe=recipe)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Viewset to work with Cart model."""

    serializer_class = CartFavoriteSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def create(self, request, *args, **kwargs):
        recipe_id = kwargs["recipe_id"]
        recipe = get_object_or_404(Recipe, id=recipe_id)
        instance, created = Cart.objects.get_or_create(
            user=request.user,
            recipe=recipe,
        )
        if created:
            serializer = self.get_serializer(instance=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        recipe_id = kwargs.get("recipe_id")
        recipe = get_object_or_404(Recipe, id=recipe_id)
        user = request.user
        instance = get_object_or_404(Cart, user=user, recipe=recipe)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
