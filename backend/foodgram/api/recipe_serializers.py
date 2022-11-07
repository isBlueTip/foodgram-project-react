import logging

from drf_extra_fields.fields import Base64ImageField
from loggers import formatter, logger_recipe_serializers
from recipes.models import Cart, Favorite, Ingredient, IngredientQuantity, Recipe, Tag
from rest_framework import serializers
from users.models import Subscription, User

LOG_NAME = "logs/logger_recipe_serializers.log"
file_handler = logging.FileHandler(LOG_NAME)
file_handler.setFormatter(formatter)
logger_recipe_serializers.addHandler(file_handler)


class AuthorSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
        ]

    def get_is_subscribed(self, instance):
        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        if Subscription.objects.filter(follower=user, author=instance).exists():
            return True
        return False


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

    # id = serializers.CharField()

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

    tags = TagSerializer(many=True, source='tag_set')
    # tags = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # tags = TagSerializer
    author = AuthorSerializer(read_only=True, default=serializers.CurrentUserDefault())
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

    def to_internal_value(self, data):
        logger_recipe_serializers.debug(f'data in beginning of my to_internal_value = {data}')
    #     raw_tags = data.get("tags")
    #     logger_recipe_serializers.debug(f'raw_tags = {raw_tags}')
    #     tags = []
    #     if raw_tags:
    #         for tag in raw_tags:
    #             tags.append({"id": tag})
    #     logger_recipe_serializers.debug(f'tags = {tags}')
    #     data["tags"] = tags
        res = super(RecipeSerializer, self).to_internal_value(data)
        return res

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
        # logger_recipe_serializers.debug(f'validated_data = {validated_data}')
        author = self.context.get("request").user
        tags = validated_data.pop("tags", None)
        # logger_recipe_serializers.debug(f'tags = {tags}')
        ingredients = validated_data.pop("ingredientquantity_set")
        instance = Recipe.objects.create(author=author, **validated_data)
        instance.tags.set([int(tag["id"]) for tag in tags])
        # tags = [tag.id for tag in tags]
        self.create_ingredients(instance, ingredients)
        return instance

    def update(self, instance, validated_data):
        logger_recipe_serializers.debug(f'validated_data_update = {validated_data}')
        tags = validated_data.pop("tags", None)
        ingredients = validated_data.pop("ingredientquantity_set")
        super().update(instance, validated_data)

        # instance.tags.set([int(tag["id"]) for tag in tags])
        logger_recipe_serializers.debug(f'[tag.id for tag in tags] = {[tag.id for tag in tags]}')
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
