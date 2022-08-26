import django_filters

from recipes.models import Recipe, Tag, Ingredient


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )
    is_favorited = django_filters.NumberFilter()
    is_in_shopping_cart = django_filters.NumberFilter()

    class Meta:
        model = Recipe
        fields = {
            'tags',
            'is_favorited',
            'is_in_shopping_cart',
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
