import django_filters

from recipes.models import Recipe, Tag, Ingredient



import logging
from loggers import logger, formatter
LOG_NAME = 'serializers.log'
file_handler = logging.FileHandler(LOG_NAME)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


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
    # is_in_shopping_cart = django_filters.NumberFilter()

    def filter_is_favorited(self, queryset, name, value):
        logger.debug(f'queryset = {queryset}')
        if int(value):
            logger.debug(f'value = 1')
            queryset = Recipe.objects.filter(is_favorited=self.user)
        # lookup = '__'.join([name, 'isnull'])
        # return queryset.filter(**{lookup: False})
        return queryset

    class Meta:
        model = Recipe
        fields = {
            'tags',
            'is_favorited',
            # 'is_in_shopping_cart',
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
