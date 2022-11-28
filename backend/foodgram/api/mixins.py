from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.recipe_serializers import CartFavoriteSerializer
from recipes.models import Cart, Favorite, Recipe


class CartFavoriteMixin(
    mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    serializer_class = CartFavoriteSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_create_queryset(self, instance):
        raise NotImplementedError

    def get_delete_queryset(self, user, instance):
        raise NotImplementedError

    def create(self, request, *args, **kwargs):
        recipe_id = kwargs.get("recipe_id")
        recipe = get_object_or_404(Recipe, id=recipe_id)
        instance, created = self.get_create_queryset(recipe)
        if created:
            serializer = self.get_serializer(instance=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        recipe_id = kwargs.get("recipe_id")
        recipe = get_object_or_404(Recipe, id=recipe_id)
        user = request.user
        instance = self.get_delete_queryset(user, recipe)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteViewSet(CartFavoriteMixin):
    def get_create_queryset(self, instance):
        return Favorite.objects.get_or_create(
            user=self.request.user,
            recipe=instance,
        )

    def get_delete_queryset(self, user, instance):
        return get_object_or_404(Favorite, user=user, recipe=instance)


class CartViewSet(CartFavoriteMixin):
    def get_create_queryset(self, instance):
        return Cart.objects.get_or_create(
            user=self.request.user,
            recipe=instance,
        )

    def get_delete_queryset(self, user, instance):
        return get_object_or_404(Cart, user=user, recipe=instance)
