# import logging

from rest_framework import serializers

# from .loggers import logger, formatter
from recipes.models import Recipe, Tag, Ingredient
from users.models import User
# from api.users_serializers import UserSerializer


# LOG_NAME = 'serializers.log'
#
# file_handler = logging.FileHandler(LOG_NAME)
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)


# class ImageField(serializers.ImageField):
#
#     def to_internal_value(self, data):
#         print(data)
#         file_object = super().to_internal_value(data)
#         django_field = self._DjangoImageField()
#         django_field.error_messages = self.error_messages
#         return django_field.clean(file_object)


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name',
                  'last_name',
                  ]


class TagSerializer(serializers.ModelSerializer):
    # color = serializers.StringRelatedField(source='tag_color')

    class Meta:
        model = Tag
        fields = ['id',
                  'name',
                  'color',
                  'slug',
                  ]


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ['id',
                  'name',
                  'color',
                  'slug',
                  ]


class RecipeSerializer(serializers.ModelSerializer):
    # # author field is not required during creating a new post
    # author = serializers.StringRelatedField(
    #     read_only=True, default=serializers.CurrentUserDefault()
    # )

    author = AuthorSerializer()
    # tags = serializers.StringRelatedField(source='tags.color',
    #                                       many=True)
    tags = TagSerializer(many=True)
    ingredients = IngredientSerializer(many=True)
    # image = serializers.ImageField()

    class Meta:
        model = Recipe
        fields = ['id',
                  'name',
                  'author',
                  'text',
                  'ingredients',
                  'cooking_time',
                  'image',
                  'tags',
                  ]


# class CommentSerializer(serializers.ModelSerializer):
#     # author field is not required during creating a new post
#     author = serializers.StringRelatedField(
#         read_only=True, default=serializers.CurrentUserDefault()
#     )
#
#     class Meta:
#         model = Comment
#         fields = ('id', 'author', 'post', 'text', 'created')
