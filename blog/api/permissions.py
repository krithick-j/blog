from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_owner

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin

class IsMember(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_member
