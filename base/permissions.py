from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    message = 'Admin access required.'

    def has_permission(self, request, view):
        from base.models import Admin
        return bool(
            request.user
            and request.user.is_authenticated
            and isinstance(request.user, Admin)
        )


class IsRegularUser(BasePermission):
    message = 'User access required.'

    def has_permission(self, request, view):
        from base.models import User
        return bool(
            request.user
            and request.user.is_authenticated
            and isinstance(request.user, User)
        )
