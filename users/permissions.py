from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.utils import timezone

from pairings.models import Emparejamiento

class IsOwnerOrCoordinadorOrPartOfMenteesOrMentor(BasePermission):
    def has_object_permission(self, request, view, obj):
        

        user = request.user
        # Coordinador puede todo
        if user.rol_actual == 'coordinador':
            return True
        # Propio usuario
        if obj == user:
            return True
        now = timezone.now()
        semester = 0
        
        if now.month in (9,10,11,12,1):
            semester = 1
        else:
            semester = 2
        # Usuario forma parte de mis mentorizados
        if user.rol_actual == 'mentor':
            return Emparejamiento.objects.filter(
                mentor=user,
                mentorizado=obj,
                year=now.year,
                cuatrimestre=semester
            ).exists()
        # Usuario es mi mentor
        if user.rol_actual == 'mentorizado':
            return Emparejamiento.objects.filter(
                mentor=obj,
                mentorizado=user,
                year=now.year,
                cuatrimestre=semester
            ).exists()
         


        return False

class IsOwnerOrCoordinador(BasePermission):
    """
    Permite acceso a los detalles de un Usuario al propio user o al coordinador.
    """
    def has_object_permission(self, request, view, obj):
        
        if request.user.rol_actual == 'coordinador':
            return True
        # el propio usuario
        return obj == request.user

class IsRoleOwnerOrCoordinador(BasePermission):
    """
    Para la app reports: solo el autor del informe o el coordinador.
    """
    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS incluyen GET, HEAD, OPTIONS
        if request.user.rol_actual == 'coordinador':
            return True
        # autor del informe
        return obj.usuario == request.user

class IsReportOwnerOrCoordinador(BasePermission):
    """
    Para la app reports: solo el autor del informe o el coordinador.
    """
    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS incluyen GET, HEAD, OPTIONS
        if request.user.rol_actual == 'coordinador':
            return True
        # autor del informe
        return obj.user == request.user

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