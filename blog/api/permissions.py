from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff  # Only staff (admin) can create/edit/delete articles


class IsMember(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated  # Only authenticated users (Members) can access articles


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True  # Admin can access any object
        return obj.author == request.user  # User can only access their own articles/comments
