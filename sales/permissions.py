# permissions.py
from rest_framework.permissions import BasePermission

class IsBaseUserOrSubuser(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user == obj.user or request.user.base_user == obj.user:
            return True
        return False
