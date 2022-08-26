from rest_framework import serializers

from recipes.models import Recipe, Tag, Ingredient, IngredientQuantity
from users.models import User

import base64
from django.core.files.base import ContentFile

import logging
from loggers import logger, formatter
LOG_NAME = 'serializers.log'
file_handler = logging.FileHandler(LOG_NAME)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):
        format, imgstr = data.split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return data


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            # 'is_subscribed',
        ]


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

    author = AuthorSerializer(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    tags = TagSerializer(
        many=True
    )
    ingredients = IngredientQuantitySerializer(
        source='ingredientquantity_set',
        many=True,
    )
    image = Base64ImageField()

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

        # read_only_fields = [
        #     'is_in_shopping_cart',
        #     'is_favorited',
        # ]

    def to_internal_value(self, data):
        # logger.debug(f'raw_data = {data}')
        raw_tags = data.pop('tags')
        tags = []
        for tag in raw_tags:
            tags.append({'id': tag})
        # logger.debug(f'tags = {tags}')
        data['tags'] = tags
        # logger.debug(f'data = {data}')
        res = super(RecipeSerializer, self).to_internal_value(data)
        # res.tags = tags
        # logger.debug(f'new_res = {res}')
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

    # def validate_tags(self, value):
    #     logger.debug(value)
    #     return value

    def create(self, validated_data):
        # logger.debug(f'validated_data = {validated_data}')
        author = self.context.get('request').user
        raw_tags = validated_data.pop('tags')
        tags = []
        for tag in raw_tags:
            tags.append(int(tag['id']))
        logger.debug(f'tags = {tags}')
        ingredients = validated_data.pop('ingredientquantity_set')
        instance = Recipe.objects.create(author=author, **validated_data)
        instance.tags.set(tags)
        for recipe_ingredient in ingredients:
            ingredient = int(recipe_ingredient['ingredient']['id'])
            ingredient = Ingredient.objects.get(id=ingredient)
            quantity = int(recipe_ingredient['quantity'])
            IngredientQuantity.objects.create(
                recipe=instance,
                ingredient=ingredient,
                quantity=quantity
            )
        return instance
