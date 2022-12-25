import logging

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from api.base_serializers import BaseUserSerializer
from api.recipe_serializers import CartFavoriteSerializer
from recipes.models import Recipe
from users.models import User

logger = logging.getLogger('logger')


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
    recipes = CartFavoriteSerializer(many=True, read_only=True)
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
        return Recipe.objects.filter(author=instance).count()
