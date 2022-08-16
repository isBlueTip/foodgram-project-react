# import logging

from rest_framework import serializers

# from .loggers import logger, formatter
from users.models import User


# LOG_NAME = 'serializers.log'
#
# file_handler = logging.FileHandler(LOG_NAME)
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['first_name',
#                   'last_name',
#                   ]


class UserSerializer(serializers.ModelSerializer):
    # # author field is not required during creating a new post
    # author = serializers.StringRelatedField(
    #     read_only=True, default=serializers.CurrentUserDefault()
    # )

    # user = serializers.StringRelatedField(source='author')
    # user = UserSerializer(source='author')

    class Meta:
        model = User
        fields = '__all__'
        # fields = ['id',
        #           'name',
        #           'user',  # TODO create user endpoints?
        #           'text',
        #           'ingredients',
        #           'cooking_time',
        #           'picture',
        #           'tags',
        #           ]


# class TagSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Tag
#         fields = ['id',
#                   'name',
#                   'hex_color',
#                   'slug',
#                   ]
#         # fields = '__all__'


# class CommentSerializer(serializers.ModelSerializer):
#     # author field is not required during creating a new post
#     author = serializers.StringRelatedField(
#         read_only=True, default=serializers.CurrentUserDefault()
#     )
#
#     class Meta:
#         model = Comment
#         fields = ('id', 'author', 'post', 'text', 'created')
