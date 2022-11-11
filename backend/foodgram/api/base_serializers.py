from rest_framework import serializers

from users.models import Subscription, User


class BaseUserSerializer(serializers.ModelSerializer):
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
        return Subscription.objects.filter(
            follower=user,
            author=instance).exists()
