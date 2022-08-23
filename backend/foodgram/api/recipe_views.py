import logging

from api.recipe_serializers import RecipeSerializer, TagSerializer, IngredientSerializer
from loggers import formatter, logger
# from .permissions import IsOwnerOrReadOnly
from recipes.models import Recipe, Tag, Ingredient
from rest_framework import viewsets  # , status
from rest_framework.response import Response
from api.filters import RecipeFilter

# from django.shortcuts import get_object_or_404

# from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated, AllowAny



LOG_NAME = 'recipes_views.log'

file_handler = logging.FileHandler(LOG_NAME)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class RecipeViewSet(viewsets.ModelViewSet):
    """Viewset to work with Recipe model."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filterset_class = RecipeFilter
    # permission_classes = [AllowAny, ]


class TagViewSet(viewsets.ModelViewSet):
    """Viewset to work with Tag model."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None  # TODO why front works only wo/ pagination?


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset to work with Recipe model."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    # filterset_class = RecipeFilter
    # permission_classes = [AllowAny, ]


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
