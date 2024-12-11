from rest_framework.permissions import BasePermission


class AddCategoryPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.has_perm('panel.add_category'))
