from django.contrib import admin

from users.models import Subscription, User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "role",
    )
    list_editable = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "role",
    )
    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )
    list_filter = (
        "is_staff",
        "role",
    )
    empty_value_display = "empty"


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "follower",
        "author",
    )
    list_editable = (
        "author",
    )
    search_fields = (
        "follower",
        "author",
    )
    empty_value_display = "empty"


admin.site.register(User, UserAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
