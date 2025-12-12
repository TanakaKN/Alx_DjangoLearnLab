from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission:
    - SAFE_METHODS (GET, HEAD, OPTIONS): allow for everyone
    - Other methods (POST, PUT, PATCH, DELETE): only if user is the object's author
    """

    def has_object_permission(self, request, view, obj):
        # Allow read-only methods for any request
        if request.method in SAFE_METHODS:
            return True

        # Write permissions are only allowed to the author of the object.
        return getattr(obj, "author", None) == request.user
