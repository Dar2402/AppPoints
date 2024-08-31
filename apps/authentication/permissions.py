from rest_framework.permissions import IsAuthenticated, IsAdminUser, SAFE_METHODS

class IsAdminOrReadOnly(IsAuthenticated):
    """
    Custom permission to only allow admins to edit objects, but allow read-only access to authenticated users.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return bool(request.user and (request.user.is_staff or request.user.is_superuser))