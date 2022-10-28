import logging

import django_filters

from loggers import formatter, logger_filters
from recipes.models import Ingredient, Recipe, Tag
from users.models import User

LOG_NAME = 'logs/logger_filters.log'
file_handler = logging.FileHandler(LOG_NAME)
file_handler.setFormatter(formatter)
logger_filters.addHandler(file_handler)


class RecipeFilter(django_filters.FilterSet):
    def __init__(self, request, *args, **kwargs):
        self.user = request.user
        super(django_filters.FilterSet, self).__init__(*args, **kwargs)

    tags = django_filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )
    is_favorited = django_filters.Filter(
        field_name='is_favorited',
        method='filter_is_favorited',
    )
    author = django_filters.ModelChoiceFilter(
        field_name='author_id',
        to_field_name='id',
        queryset=User.objects.all(),
    )

    def filter_is_favorited(self, queryset, name, value):
        if value == '0':
            return queryset
        queryset = queryset.filter(favorite__user=self.user)
        return queryset

    class Meta:
        model = Recipe
        fields = {
            'tags',
        }


class IngredientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='istartswith'
    )

    class Meta:
        model = Ingredient
        fields = {
            'name',
        }
