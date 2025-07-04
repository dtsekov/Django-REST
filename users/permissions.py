from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrCoordinador(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Coordinador puede todo, el propio usuario puede ver o editar
        if request.user.rol_actual == 'coordinador':
            return True
        return obj == request.user

class IsCoordinador(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol_actual == 'coordinador'