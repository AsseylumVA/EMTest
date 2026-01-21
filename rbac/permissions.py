from rest_framework import permissions

from utils.permissions import PermissionChecker


class IsAdmin(permissions.BasePermission):
    message = 'Only administrators can access this resource.'

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        checker = PermissionChecker(request.user)
        return checker.is_admin()


class HasElementPermission(permissions.BasePermission):

    ACTION_MAP = {
        'GET': 'read',
        'HEAD': 'read',
        'OPTIONS': 'read',
        'POST': 'create',
        'PUT': 'update',
        'PATCH': 'update',
        'DELETE': 'delete',
    }

    def has_permission(self, request, view):
        element_code = getattr(view, 'element_code', None)
        if not element_code:
            return False

        action = self.ACTION_MAP.get(request.method)
        if not action:
            return False

        checker = PermissionChecker(request.user)
        return checker.has_permission(element_code, action)

    def has_object_permission(self, request, view, obj):
        element_code = getattr(view, 'element_code', None)
        if not element_code:
            return False

        action = self.ACTION_MAP.get(request.method)
        if not action:
            return False

        checker = PermissionChecker(request.user)
        return checker.has_permission(element_code, action, obj)
