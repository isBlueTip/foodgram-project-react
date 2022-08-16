# import logging

from rest_framework import serializers

# from .loggers import logger, formatter
from recipes.models import Recipe, Tag


# LOG_NAME = 'serializers.log'
#
# file_handler = logging.FileHandler(LOG_NAME)
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)


class RecipeSerializer(serializers.ModelSerializer):
    # # author field is not required during creating a new post
    # author = serializers.StringRelatedField(
    #     read_only=True, default=serializers.CurrentUserDefault()
    # )

    class Meta:
        model = Recipe
        # fields = ('id', 'name', 'author', 'text')
        # fields = ('recipes', )
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        # fields = ('title', 'slug', 'description')
        fields = '__all__'


# class CommentSerializer(serializers.ModelSerializer):
#     # author field is not required during creating a new post
#     author = serializers.StringRelatedField(
#         read_only=True, default=serializers.CurrentUserDefault()
#     )
#
#     class Meta:
#         model = Comment
#         fields = ('id', 'author', 'post', 'text', 'created')
