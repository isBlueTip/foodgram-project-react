import logging

# from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated

from loggers import logger, formatter
# from .permissions import IsOwnerOrReadOnly
from recipes.models import Recipe, Tag
from api.serializers import RecipeSerializer, TagSerializer


LOG_NAME = 'api.views.log'

file_handler = logging.FileHandler(LOG_NAME)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class RecipeViewSet(viewsets.ModelViewSet):
    """Viewset to work with Recipe model."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    # pagination_class = PageLimitPagination
    # permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def retrieve(self, request, *args, **kwargs):

        instance = self.get_object()
        logger('HERE')
        print(instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
        # serializer = RecipeSerializer(
        #     data=request.data, context={'request': request})
        # logger.debug(serializer)
        # if serializer.is_valid():
        #     serializer.save(author=request.user)
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # def create(self, request, *args, **kwargs):
    #     serializer = RecipeSerializer(
    #         data=request.data, context={'request': request})
    #     # logger.debug(serializer)
    #     if serializer.is_valid():
    #         serializer.save(author=request.user)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagViewSet(viewsets.ModelViewSet):
    """Viewset to work with Tag model."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


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
