import logging

from django.db.models import Sum
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from api.filters import IngredientFilter, RecipeFilter
from api.permissions import IsAdminOrIsAuthorOrReadOnly
from api.recipe_serializers import (IngredientSerializer, RecipeSerializer,
                                    TagSerializer)
from recipes.models import Ingredient, IngredientQuantity, Recipe, Tag

logger = logging.getLogger('logger')


class RecipeViewSet(viewsets.ModelViewSet):

    queryset = Recipe.objects.all()
    filterset_class = RecipeFilter
    serializer_class = RecipeSerializer
    permission_classes = [
        IsAdminOrIsAuthorOrReadOnly,
    ]

    @action(
        detail=False,
        methods=[
            "get",
        ],
        permission_classes=[
            IsAuthenticated,
        ],
        url_path="download_shopping_cart",
    )
    def cart(self, request):
        user = request.user
        cart = (
            IngredientQuantity.objects.values(
                "ingredient__name",
                "quantity",
                "ingredient__measurement_unit",
            )
            .order_by("ingredient__id").filter(recipe__cart__user=user)
            .annotate(total=Sum("ingredient__ingredientquantity__quantity"))
        )
        ingredients = {}
        for ingredient in cart:
            name = ingredient["ingredient__name"]
            if name in ingredients:
                continue
            total = ingredient["total"]
            units = ingredient["ingredient__measurement_unit"]
            ingredients[name] = [total, units]

        response = HttpResponse(content_type="text/plain; charset=utf-8")
        response["Content-Disposition"] = "attachment;" ' filename="shopping_list.txt"'
        for index, ingredient in enumerate(ingredients):
            response.write(
                f"{index + 1}. {ingredient}: "
                f"{ingredients[ingredient][0]} {ingredients[ingredient][1]}\n"
            )
        response.write("Приятного аппетита!")
        return response


class TagViewSet(viewsets.ModelViewSet):

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = [
        IsAdminOrIsAuthorOrReadOnly,
    ]


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filterset_class = IngredientFilter
    pagination_class = None
