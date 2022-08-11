from django.contrib import admin

from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'username',
                    'email',
                    'first_name',
                    'last_name',
                    'is_staff',
                    'role',
                    'confirmation_code',
                    )
    list_editable = ('username',
                     'email',
                     'first_name',
                     'last_name',
                     'is_staff',
                     'role',
                     'confirmation_code',
                     )
    search_fields = ('username',
                     'email',
                     'first_name',
                     'last_name',
                     )
    list_filter = ('is_staff',
                   'role',
                   )
    empty_value_display = 'empty'


admin.site.register(User, UserAdmin)
