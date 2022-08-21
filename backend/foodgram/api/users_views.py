import logging

from api.users_serializers import (CreateUserSerializer, PasswordSerializer,
                                   UserSerializer)
from loggers import formatter, logger
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
# from .permissions import IsOwnerOrReadOnly
from users.models import ADMIN, USER, User

LOG_NAME = 'users_views.log'

file_handler = logging.FileHandler(LOG_NAME)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class UserViewSet(viewsets.ModelViewSet):
    """Viewset to work with User model."""

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False,
            methods=['get', ],
            permission_classes=[IsAuthenticated, ],
            url_path='me',
            name='View current user details')
    def view_user_info(self, request):
        user = self.request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False,
            methods=['post', ],
            permission_classes=[IsAuthenticated, ],
            serializer_class=PasswordSerializer,
            url_path='set_password',
            name='Change current user password')
    def set_user_password(self, request):
        user = self.request.user
        serializer = self.get_serializer(data=self.request.data)
        if serializer.is_valid(raise_exception=True):
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
