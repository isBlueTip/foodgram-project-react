from rest_framework.permissions import (SAFE_METHODS, BasePermission,
                                        IsAuthenticatedOrReadOnly)


class RegisterOrIsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.method == 'POST' or
            request.user and
            request.user.is_authenticated
        )


class IsAdminOrIsAuthorOrReadOnly(IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj):
        return bool(request.method in SAFE_METHODS or
                    obj.author == request.user or
                    request.user.is_staff
                    )
