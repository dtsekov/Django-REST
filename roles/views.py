from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import SolicitudRol
from .serializers import SolicitudRolSerializer
from users.permissions import IsCoordinador, IsRoleOwnerOrCoordinador
from django.utils import timezone

class SolicitudRolViewSet(viewsets.ModelViewSet):
    queryset = SolicitudRol.objects.all()
    serializer_class = SolicitudRolSerializer


    def get_queryset(self):
        user = self.request.user
        qs = SolicitudRol.objects.all()
        now = timezone.now()
        semester = 0
        if now.month in (9,10,11,12,1):
            semester = 1
        else:
            semester = 2
        # Coordinator sees all for current year and semester via emparejamiento
        if user.rol_actual == 'coordinador':
            return qs.filter(
                year=now.year,
                cuatrimestre=semester
            )
        # 
        if user.rol_actual == 'mentor':
            return qs.filter(
            usuario=user,
            year=now.year,
            cuatrimestre=semester
            )
        return qs.filter(
            usuario=user,
            year=now.year,
            cuatrimestre=semester
        )
    
    def perform_create(self, serializer):
        # En create no se pasa year/cuatrimestre, queda auto en save()
        serializer.save()

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        if self.action == 'list':
            return [IsAuthenticated()]
        if self.action == 'retrieve':
            return [IsRoleOwnerOrCoordinador()]
        if self.action == 'partial_update':
            return [IsCoordinador()]
        return [IsAuthenticated()]

    def partial_update(self, request, *args, **kwargs):
        # Coordinador cambia estado y comentario
        instance = self.get_object()
        data = request.data
        instance.estado = data.get('estado', instance.estado)
        instance.comentario_coordinador = data.get('comentario_coordinador', instance.comentario_coordinador)
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)