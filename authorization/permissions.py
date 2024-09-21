from rest_framework.permissions import BasePermission

from authorization import choices as authorization_choices


class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == authorization_choices.UserChoices.ADMIN


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == authorization_choices.UserChoices.USER


class AdminOrSelf(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_admin:
            return True
        return obj.user_id == request.user.user_id
