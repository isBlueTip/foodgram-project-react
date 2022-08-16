import logging

# from django.shortcuts import get_object_or_404

from rest_framework import viewsets  # , status
from rest_framework.response import Response
# from rest_framework.pagination import LimitOffsetPagination
# from rest_framework.permissions import IsAuthenticated

from loggers import logger, formatter
# from .permissions import IsOwnerOrReadOnly
from users.models import User
from api.users_serializers import UserSerializer


LOG_NAME = 'users_views.log'

file_handler = logging.FileHandler(LOG_NAME)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class UserViewSet(viewsets.ModelViewSet):
    """Viewset to work with Recipe model."""

    queryset = User.objects.all()
    serializer_class = UserSerializer

    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         logger.debug(f'serializer = {serializer}')
    #         logger.debug(f'serializer.data = {serializer.data}')
    #         return self.get_paginated_response(serializer.data)
    #
    #     serializer = self.get_serializer(queryset, many=True)
    #     logger.debug(f'serializer = {serializer}')
    #     logger.debug(f'serializer.data = {serializer.data}')
    #     return Response(serializer.data)


# class TagViewSet(viewsets.ModelViewSet):
#     """Viewset to work with Tag model."""
#
#     queryset = Tag.objects.all()
#     serializer_class = TagSerializer
#     pagination_class = None  # TODO why tags work only wo/ pagination?


# class CommentViewSet(viewsets.ModelViewSet):
#     """Viewset to work with Comment model."""
#
#     serializer_class = CommentSerializer
#     permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
#
#     def get_queryset(self):
#         post_id = self.kwargs.get('post_id')
#         post = get_object_or_404(Post, pk=post_id)
#         comments = post.comments
#         return comments
#
#     def create(self, request, *args, **kwargs):
#         serializer = CommentSerializer(
#             data=request.data, context={'request': request})
#         logger.debug(serializer)
#         if serializer.is_valid():
#             serializer.save(author=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
