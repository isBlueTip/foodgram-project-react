import logging

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from api.base_serializers import BaseUserSerializer
from api.recipe_serializers import CartFavoriteSerializer
from loggers.loggers import formatter, logger_users_serializers
from recipes.models import Recipe
from users.models import User

LOG_NAME = "logs/logger_users_serializers.log"

file_handler = logging.FileHandler(LOG_NAME)
file_handler.setFormatter(formatter)
logger_users_serializers.addHandler(file_handler)


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "id": {"read_only": True},
        }

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class PasswordSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            "current_password",
            "new_password",
        ]

    def validate_current_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                {"current_password": "current password is incorrect"}
            )
        return value

    def validate_new_password(self, value):
        user = self.context["request"].user
        validate_password(value, user)
        return value


class SubscriptionSerializer(BaseUserSerializer):
    recipes = CartFavoriteSerializer(many=True,
                                     read_only=True, source="recipe")
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "recipes",
            "recipes_count",
        ] + BaseUserSerializer.Meta.fields

        read_only_fields = [
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
        ]

    def get_recipes_count(self, instance):
        return len(Recipe.objects.filter(author=instance))
