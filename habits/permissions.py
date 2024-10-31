from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrPublicReadOnly(BasePermission):
    """
    Разрешает доступ к объекту только его владельцу, либо доступ только для чтения для публичных объектов.
    """

    def has_object_permission(self, request, view, obj):
        # Разрешение на чтение для публичных привычек
        if obj.is_public and request.method in SAFE_METHODS:
            return True

        # Разрешение на доступ только владельцу объекта
        if obj.user == request.user:
            return True

        return False
