from rest_framework.permissions import BasePermission

class IsAdminUserRole(BasePermission):
    """
    Custom permission to allow access only to users with the 'admin' role.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and has the 'admin' role
        return bool(request.user and request.user.is_authenticated and request.user.role == 'admin')