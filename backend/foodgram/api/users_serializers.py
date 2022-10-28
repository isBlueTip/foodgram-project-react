import logging
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from loggers import logger_users_serializers, formatter
from users.models import User, Subscription
from recipes.models import Recipe
from api.recipe_serializers import CartFavoriteSerializer, RecipeSerializer

LOG_NAME = 'logger_users_serializers.log'

file_handler = logging.FileHandler(LOG_NAME)
file_handler.setFormatter(formatter)
logger_users_serializers.addHandler(file_handler)


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        ]
        extra_kwargs = {
                'password': {'write_only':   True},
                'id': {'read_only':          True},
        }

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email',
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


class PasswordSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['current_password',
                  'new_password',
                  ]

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({'current_password': 'current password is incorrect'})
        return value

    def validate_new_password(self, value):
        user = self.context['request'].user
        validate_password(value, user)
        return value


class SubscriptionSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = CartFavoriteSerializer(many=True, read_only=True, source='recipe')
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        ]

        read_only_fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
        ]

    def get_is_subscribed(self, instance):
        user = self.context.get('request').user
        try:
            Subscription.objects.get(follower=user, author=instance)
        except Subscription.DoesNotExist:
            return False
        return True

    def get_recipes_count(self, instance):
        return len(Recipe.objects.filter(author=instance))
