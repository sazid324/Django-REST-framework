from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user


class IsOwnerOrAdminUpdate(permissions.BasePermission):
    """
    Custom permission to allow only the owner or admin to update the object.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.created_by == request.user or request.user.is_staff


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsProtected(permissions.BasePermission):
    """
    Custom permission to allow only the owner or admin to update the object.
    """

    def has_permission(self, request, view):
        return request.user and not request.user.is_user


class IsAdmin(permissions.BasePermission):
    """
    Custom permission to allow only the owner or admin to update the object.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_admin


class IsUser(permissions.BasePermission):
    """
    Custom permission to allow only the owner or admin to update the object.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_user
