from rest_framework import permissions
class   IsAdmin(permissions.BasePermission):
    """
    Permission for Admin users.
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role in ['admin', 'owner', 'super_admin']
        return False
        # return request.user and request.user.role in ['admin', 'owner', 'super_admin']

class IsMember(permissions.BasePermission):
    """
    Permission for Member users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.role in ['member', 'admin', 'owner', 'super_admin']

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True  # Admin can access any object
        return obj.author == request.user  # User can only access their own articles/comments
