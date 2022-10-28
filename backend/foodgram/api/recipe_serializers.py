from rest_framework import serializers

from recipes.models import Recipe, Tag, Ingredient, IngredientQuantity, Favorite, Cart
from users.models import User, Subscription

from drf_extra_fields.fields import Base64ImageField

import logging
from loggers import logger_recipe_serializers, formatter
LOG_NAME = 'logger_recipe_serializers.log'
file_handler = logging.FileHandler(LOG_NAME)
file_handler.setFormatter(formatter)
logger_recipe_serializers.addHandler(file_handler)


class AuthorSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        ]

    def get_is_subscribed(self, instance):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        try:
            Subscription.objects.get(follower=user, author=instance)
        except Subscription.DoesNotExist:
            return False
        return True


class IngredientQuantitySerializer(serializers.ModelSerializer):

    id = serializers.CharField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')
    amount = serializers.CharField(source='quantity')

    class Meta:
        model = IngredientQuantity
        fields = [
            'id',
            'name',
            'measurement_unit',
            'amount',
        ]


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = [
            'id',
            'name',
            'measurement_unit',
        ]


class TagSerializer(serializers.ModelSerializer):

    id = serializers.CharField()

    class Meta:
        model = Tag
        fields = [
            'id',
            'name',
            'color',
            'slug',
        ]

        read_only_fields = [
            'name',
            'color',
            'slug',
        ]

        write_only_fields = ['id', ]


class RecipeSerializer(serializers.ModelSerializer):

    tags = TagSerializer(
        many=True
    )
    author = AuthorSerializer(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    ingredients = IngredientQuantitySerializer(
        source='ingredientquantity_set',
        many=True,
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField(required=True)

    class Meta:
        model = Recipe
        fields = [
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        ]

    def get_is_favorited(self, instance):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        try:
            Favorite.objects.get(user=user, recipe=instance)
        except Favorite.DoesNotExist:
            return False
        return True

    def get_is_in_shopping_cart(self, instance):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        try:
            Cart.objects.get(user=user, recipe=instance)
        except Cart.DoesNotExist:
            return False
        return True

    def to_internal_value(self, data):
        raw_tags = data.get('tags')
        tags = []
        if raw_tags:
            for tag in raw_tags:
                tags.append({'id': tag})
        data['tags'] = tags
        res = super(RecipeSerializer, self).to_internal_value(data)
        return res

    def validate_ingredients(self, value):
        # logger.debug(value)
        for recipe_ingredient in value:
            ingredient = int(recipe_ingredient['ingredient']['id'])
            try:
                ingredient = Ingredient.objects.get(id=ingredient)  # TODO KISS! I make a whole db request only just to validate and repeat this action in def create()!
            except Exception as e:
                msg = f'ингредиента с номером {ingredient} нет в списке'
                raise serializers.ValidationError(msg)
        return value  # TODO return cleaned data with instances instead of IDs?


    def create_ingredients(self, instance, ingredients):
        for recipe_ingredient in ingredients:
            ingredient = int(recipe_ingredient['ingredient']['id'])
            ingredient = Ingredient.objects.get(id=ingredient)
            quantity = int(recipe_ingredient['quantity'])
            IngredientQuantity.objects.create(
                recipe=instance,
                ingredient=ingredient,
                quantity=quantity
            )

    def create(self, validated_data):
        author = self.context.get('request').user
        raw_tags = validated_data.pop('tags')
        tags = []
        for tag in raw_tags:
            tags.append(int(tag['id']))
        ingredients = validated_data.pop('ingredientquantity_set')
        instance = Recipe.objects.create(author=author, **validated_data)
        instance.tags.set(tags)
        self.create_ingredients(instance, ingredients)
        return instance

    def update(self, instance, validated_data):  # TODO IsAuthorOrReadOnly permission
        raw_tags = validated_data.pop('tags', None)
        tags = []
        for tag in raw_tags:
            tags.append(int(tag['id']))
        ingredients = validated_data.pop('ingredientquantity_set')

        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.tags.set(tags)
        IngredientQuantity.objects.filter(recipe=instance).delete()
        self.create_ingredients(instance, ingredients)
        instance.save()
        return instance


class CartFavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = [
            'id',
            'name',
            'image',
            'cooking_time',
        ]

        read_only_fields = [
            'id',
            'name',
            'image',
            'cooking_time',
        ]
