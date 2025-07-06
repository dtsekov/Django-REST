from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrCoordinador(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Coordinador puede todo, el propio usuario puede ver o editar
        if request.user.rol_actual == 'coordinador':
            return True
        return obj == request.user

class IsReportOwnerOrCoordinador(BasePermission):
    """
    Para la app reports: solo el autor del informe (respuesta_general) o el coordinador.
    """
    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS incluyen GET, HEAD, OPTIONS
        if request.user.rol_actual == 'coordinador':
            return True
        # autor del informe
        return obj.respuesta_general == request.user

class IsPairingOwnerOrCoordinador(BasePermission):
    """
    Para la app pairings: solo el mentor o el mentorizado implicado, o el coordinador.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.rol_actual == 'coordinador':
            return True
        if request.user.rol_actual == 'mentor' and obj.mentor == request.user:
            return True
        if request.user.rol_actual == 'mentorizado' and obj.mentorizado == request.user:
            return True
        return False

class IsCoordinador(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol_actual == 'coordinador'
    
class IsMentorOrMentorizado(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.rol_actual == 'mentor' or request.user.rol_actual == 'mentorizado')
class IsMentorOrMentorizadoOrCoordinador(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.rol_actual == 'mentor' or request.user.rol_actual == 'mentorizado' or request.user.rol_actual == 'coordinador')