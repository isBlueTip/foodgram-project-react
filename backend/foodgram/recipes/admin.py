from django.contrib import admin

from recipes.models import Ingredient, IngredientQuantity, Recipe, Tag


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'name',
                    'units',
                    )
    list_editable = ('name',
                     'units',
                     )
    search_fields = ('name',)
    list_filter = ('units',)
    empty_value_display = 'empty'


class IngredientInline(admin.TabularInline):

    model = IngredientQuantity
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientInline,)
    list_display = ('pk',
                    'name',
                    'author',
                    'picture',
                    'text',
                    'get_ingredients_list',
                    'get_tags_list',
                    'cooking_time',
                    )
    list_editable = ('name',
                     'author',
                     'picture',
                     'text',
                     'cooking_time',
                     )
    search_fields = ('name',
                     # 'author__name',  # TODO add lookup method for foreignkey fields
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
                    'hex_color',
                    'slug',
                    )
    list_editable = ('name',
                     'hex_color',
                     'slug',
                     )
    search_fields = ('name',
                     'hex_color',
                     'slug',
                     )
    empty_value_display = 'empty'


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
