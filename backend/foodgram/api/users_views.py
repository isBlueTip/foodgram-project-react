import logging

from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.permissions import IsAuthenticatedOrReadOnlyOrRegister
from api.users_serializers import (BaseUserSerializer, CreateUserSerializer,
                                   PasswordSerializer, SubscriptionSerializer)
from users.models import Subscription, User

logger = logging.getLogger('logger')


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnlyOrRegister]

    def get_serializer_class(self):
        if self.action == "subscriptions":
            return SubscriptionSerializer
        if self.action == "create":
            return CreateUserSerializer
        else:
            return BaseUserSerializer

    @action(
        detail=False,
        methods=[
            "get",
        ],
        permission_classes=[
            IsAuthenticated,
        ],
        url_path="me",
        url_name="me",
        name="View current user details",
    )
    def view_user_info(self, request):
        user = self.request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=[
            "post",
        ],
        permission_classes=[
            IsAuthenticated,
        ],
        serializer_class=PasswordSerializer,
        url_path="set_password",
        name="Change current user password",
    )
    def set_user_password(self, request):
        user = self.request.user
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data["new_password"])
        user.save()
        return Response(status=status.HTTP_201_CREATED)

    @action(
        detail=False,
        methods=[
            "get",
        ],
    )
    def subscriptions(self, request, *args, **kwargs):
        queryset = User.objects.filter(subscription__follower=request.user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SubscriptionViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):

    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        follower = self.request.user
        users = User.objects.all()
        following_authors = users.filter(subscription__follower=follower)
        return following_authors

    def create(self, request, *args, **kwargs):
        author_id = kwargs.get("user_id")
        author = get_object_or_404(User, id=author_id)
        if author == request.user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        instance, created = Subscription.objects.get_or_create(
            follower=request.user, author=author
        )
        if created:
            serializer = self.get_serializer(instance=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        author_id = kwargs.get("user_id")
        author = get_object_or_404(User, id=author_id)
        instance = get_object_or_404(Subscription,
                                     follower=request.user, author=author)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
