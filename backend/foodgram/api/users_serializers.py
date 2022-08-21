# import logging
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
# from .loggers import logger, formatter
from users.models import User

# LOG_NAME = 'serializers.log'
#
# file_handler = logging.FileHandler(LOG_NAME)
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)


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

    # is_subscribed =  # TODO check subscription status if authorised

    class Meta:
        model = User
        fields = '__all__'
        # fields = ['id',
        #           'username',
        #           'first_name',
        #           'last_name',
        #           # 'is_subscribed',
        #           ]


class PasswordSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['current_password',
                  'new_password',
                  ]

    def validate_current_password(self, value):
        print(self.context)
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({'current_password': 'current password is incorrect'})
        return value

    def validate_new_password(self, value):
        user = self.context['request'].user
        validate_password(value, user)
        return value
