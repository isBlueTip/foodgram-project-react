from django import forms
from django.contrib import admin

from recipes.models import Ingredient, Recipe, Tag


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


class TagAdminForm(forms.ModelForm):
    def formfield_for_tag(self, db_field, request, **kwargs):
        if db_field.name == 'tag':
            kwargs['queryset'] = Recipe.objects.filter(tag=request.tag)
        return super().formfield_for_manytomany(db_field, request, **kwargs)


# class IngredientAdminForm(forms.ModelForm):
#     def formfield_for_tag(self, db_field, request, **kwargs):
#         if db_field.name == 'tag':
#             kwargs['queryset'] = Recipe.objects.filter(tag=request.ingredient)
#         return super().formfield_for_manytomany(db_field, request, **kwargs)


class RecipeAdmin(admin.ModelAdmin):
    form = TagAdminForm
    # form = IngredientAdminForm
    list_display = ('pk',
                    'name',
                    'author',
                    'picture',
                    'text',
                    # 'ingredients',
                    'cooking_time',
                    # 'tag',
                    )
    list_editable = ('name',
                     'author',
                     'picture',
                     'text',
                     # 'ingredients',
                     'cooking_time',
                     # 'tag',
                     )
    search_fields = ('name',
                     'author',
                     'text',
                     # 'ingredients',
                     'cooking_time',
                     # 'tag',
                     )
    list_filter = ('cooking_time',
                   # 'tag',
                   )
    empty_value_display = '-empty-'


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
