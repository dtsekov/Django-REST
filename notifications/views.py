from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.permissions import IsCoordinador
from .models import Notification
from .serializers import NotificationSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    """Permite crear, listar y marcar notificaciones como leídas."""
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Solo notificaciones del usuario autenticado
        return Notification.objects.filter(usuario=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        # Permite actualizar solo el campo 'leida'
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def get_permissions(self):
        if self.action == 'create':
            return [IsCoordinador()]
        if self.action == 'retrieve':
            return [IsAuthenticated()]
        return [IsAuthenticated()]