from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import SolicitudRol
from .serializers import SolicitudRolSerializer
from users.permissions import IsCoordinador, IsRoleOwnerOrCoordinador

class SolicitudRolViewSet(viewsets.ModelViewSet):
    queryset = SolicitudRol.objects.all()
    serializer_class = SolicitudRolSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        if self.action == 'list':
            return [IsCoordinador()]
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