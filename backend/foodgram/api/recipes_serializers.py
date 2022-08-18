# import logging

from rest_framework import serializers

# from .loggers import logger, formatter
from recipes.models import Recipe, Tag
from users.models import User
# from api.users_serializers import UserSerializer


# LOG_NAME = 'serializers.log'
#
# file_handler = logging.FileHandler(LOG_NAME)
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)


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
        # fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    # # author field is not required during creating a new post
    # author = serializers.StringRelatedField(
    #     read_only=True, default=serializers.CurrentUserDefault()
    # )

    author = AuthorSerializer()
    # tags = serializers.StringRelatedField(source='tags.color',
    #                                       many=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ['id',
                  'name',
                  'author',  # TODO create user endpoints?
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
