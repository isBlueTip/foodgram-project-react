import logging

from drf_extra_fields.fields import Base64ImageField
from loggers import formatter, logger_recipe_serializers
from recipes.models import Cart, Favorite, Ingredient, IngredientQuantity, Recipe, Tag
from rest_framework import serializers
from api.base_serializers import BaseUserSerializer

from collections import OrderedDict

LOG_NAME = "logs/logger_recipe_serializers.log"
file_handler = logging.FileHandler(LOG_NAME)
file_handler.setFormatter(formatter)
logger_recipe_serializers.addHandler(file_handler)


class IngredientQuantitySerializer(serializers.ModelSerializer):

    id = serializers.CharField(source="ingredient.id")
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(source="ingredient.measurement_unit")
    amount = serializers.CharField(source="quantity")

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

    id = serializers.CharField()

    class Meta:
        model = Tag
        fields = [
            "id",
            "name",
            "color",
            "slug",
        ]

        read_only_fields = [
            "is",
            "name",
            "color",
            "slug",
        ]

        write_only_fields = [
            "id",
        ]


class RecipeSerializer(serializers.ModelSerializer):

    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    author = BaseUserSerializer(read_only=True, default=serializers.CurrentUserDefault())
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
        if Favorite.objects.filter(user=user, recipe=instance).exists():
            return True
        return False

    def get_is_in_shopping_cart(self, instance):
        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        if Cart.objects.filter(user=user, recipe=instance).exists():
            return True
        return False

    def to_representation(self, instance):
        ret = super(RecipeSerializer, self).to_representation(instance)

        for i, tag in enumerate(ret["tags"]):
            tag = Tag.objects.get(id=tag)
            ret["tags"][i] = OrderedDict()
            ret["tags"][i]['id'] = str(tag.id)
            ret["tags"][i]['name'] = tag.name
            ret["tags"][i]['color'] = tag.color
            ret["tags"][i]['slug'] = tag.slug
        return ret

    def validate_ingredients(self, value):
        pk_list = [int(ingredient['ingredient']['id']) for ingredient in value]
        for pk in pk_list:
            ingredient = Ingredient.objects.filter(id=pk)
            if pk_list.count(pk) > 1:
                msg = f"ингредиент с номером {pk} в рецепте может быть только один"
                raise serializers.ValidationError(msg)
            if not ingredient.exists():
                msg = f"ингредиента с номером {pk} нет в списке"
                raise serializers.ValidationError(msg)
        return value

    def create_ingredients(self, instance, ingredients):

        ingredinets_bulk = []

        for recipe_ingredient in ingredients:
            ingredient = Ingredient.objects.get(
                id=int(recipe_ingredient["ingredient"]["id"]))
            quantity = int(recipe_ingredient["quantity"])
            ingredinets_bulk.append([ingredient, quantity])
        obj = IngredientQuantity.objects.bulk_create(
            [(IngredientQuantity(recipe=instance, ingredient=item[0], quantity=item[1],)) for item in ingredinets_bulk]
        )

    def create(self, validated_data):
        author = self.context.get("request").user
        tags = validated_data.pop("tags", None)
        ingredients = validated_data.pop("ingredientquantity_set")
        instance = Recipe.objects.create(author=author, **validated_data)
        if tags:
            instance.tags.set([tag.id for tag in tags])
        self.create_ingredients(instance, ingredients)
        return instance

    def update(self, instance, validated_data):
        tags = validated_data.pop("tags", None)
        ingredients = validated_data.pop("ingredientquantity_set")
        super().update(instance, validated_data)
        if tags:
            instance.tags.set([tag.id for tag in tags])

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
