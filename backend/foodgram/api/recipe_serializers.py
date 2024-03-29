import logging

from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from api.base_serializers import BaseUserSerializer
from recipes.models import (Cart, Favorite, Ingredient, IngredientQuantity,
                            Recipe, Tag)

logger = logging.getLogger('logger')


class IngredientQuantitySerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(source="ingredient.id")
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(source="ingredient.measurement_unit")
    amount = serializers.IntegerField(source="quantity")

    class Meta:
        model = IngredientQuantity
        fields = [
            "id",
            "name",
            "measurement_unit",
            "amount",
        ]


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = [
            "id",
            "name",
            "measurement_unit",
        ]


class TagSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()

    class Meta:
        model = Tag
        fields = [
            "id",
            "name",
            "color",
            "slug",
        ]


class RecipeSerializer(serializers.ModelSerializer):

    tags = serializers.PrimaryKeyRelatedField(many=True,
                                              queryset=Tag.objects.all())
    author = BaseUserSerializer(
        read_only=True, default=serializers.CurrentUserDefault()
    )
    ingredients = IngredientQuantitySerializer(
        source="ingredientquantity_set",
        many=True,
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField(required=True)

    class Meta:
        model = Recipe
        fields = [
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        ]

    def get_is_favorited(self, instance):
        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        return Favorite.objects.filter(user=user, recipe=instance).exists()

    def get_is_in_shopping_cart(self, instance):
        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        return Cart.objects.filter(user=user, recipe=instance).exists()

    def validate(self, attrs):
        ret = super(RecipeSerializer, self).validate(attrs)
        ingredients = attrs.get("ingredientquantity_set")
        pk_list = [int(ingredient["ingredient"]["id"]) for ingredient in ingredients]

        for pk in pk_list:
            ingredient = Ingredient.objects.filter(id=pk)
            if pk_list.count(pk) > 1:
                msg = f"ингредиент с номером {pk}" f" в рецепте может быть только один"
                raise serializers.ValidationError(msg)
            if not ingredient.exists():
                msg = f"ингредиента с номером {pk} нет в списке"
                raise serializers.ValidationError(msg)

        for ingredient in ingredients:
            if ingredient.get("quantity") < 0:
                raise serializers.ValidationError("Количество ингредиента не может быть отрицательным!")
        return ret

    def to_representation(self, instance):
        ret = super(RecipeSerializer, self).to_representation(instance)
        tags = Tag.objects.filter(recipe=instance)
        data = TagSerializer(many=True).to_representation(tags)
        ret["tags"] = data
        return ret

    def create_ingredients(self, instance, ingredients):

        ingredients_bulk = []

        for recipe_ingredient in ingredients:
            ingredient_id = int(recipe_ingredient["ingredient"]["id"])
            quantity = int(recipe_ingredient["quantity"])
            ingredients_bulk.append([ingredient_id, quantity])
        IngredientQuantity.objects.bulk_create(
            [
                (
                    IngredientQuantity(
                        recipe=instance,
                        ingredient_id=item[0],
                        quantity=item[1],
                    )
                )
                for item in ingredients_bulk
            ]
        )

    def create(self, validated_data):
        author = self.context.get("request").user
        tags = validated_data.pop("tags", None)
        ingredients = validated_data.pop("ingredientquantity_set")
        instance = Recipe.objects.create(author=author, **validated_data)
        if tags:
            instance.tags.set([*tags])
        self.create_ingredients(instance, ingredients)
        return instance

    def update(self, instance, validated_data):
        tags = validated_data.pop("tags", None)
        ingredients = validated_data.pop("ingredientquantity_set")
        super().update(instance, validated_data)
        if tags:
            instance.tags.set([*tags])

        IngredientQuantity.objects.filter(recipe=instance).delete()
        self.create_ingredients(instance, ingredients)
        instance.save()
        return instance


class CartFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            "id",
            "name",
            "image",
            "cooking_time",
        ]

        read_only_fields = [
            "id",
            "name",
            "image",
            "cooking_time",
        ]
