from django.contrib import admin

from recipes.models import Ingredient, IngredientQuantity, Recipe, Tag


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'name',
                    'measurement_unit',
                    )
    list_editable = ('name',
                     'measurement_unit',
                     )
    search_fields = ('name',)
    list_filter = ('measurement_unit',)
    empty_value_display = 'empty'


class IngredientInline(admin.TabularInline):

    model = IngredientQuantity
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientInline,)
    list_display = ('pk',
                    'name',
                    'author',
                    'image',
                    'text',
                    'get_ingredients_list',
                    'get_tags_list',
                    'cooking_time',
                    )
    list_editable = ('name',
                     'author',
                     'image',
                     'text',
                     'cooking_time',
                     )
    search_fields = ('name',
                     # 'author__get_full_name()',  # TODO add lookup method for foreignkey fields
                     'text',
                     # 'ingredients',
                     'cooking_time',
                     )
    list_filter = ('author',  # TODO same here
                   'cooking_time',
                   )
    empty_value_display = 'empty'


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'name',
                    'color',
                    'slug',
                    )
    list_editable = ('name',
                     'color',
                     'slug',
                     )
    search_fields = ('name',
                     'color',
                     'slug',
                     )
    empty_value_display = 'empty'


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
