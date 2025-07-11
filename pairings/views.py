from rest_framework import viewsets
from users.permissions import IsCoordinador, IsOwnerOrCoordinador, IsMentorOrMentorizado, IsMentorOrMentorizadoOrCoordinador, IsPairingOwnerOrCoordinador
from .models import Emparejamiento
from .serializers import EmparejamientoSerializer
from django.utils import timezone

class EmparejamientoViewSet(viewsets.ModelViewSet):
    queryset = Emparejamiento.objects.all()
    serializer_class = EmparejamientoSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Emparejamiento.objects.all()
        now = timezone.now()
        semester = 0
        if now.month in (9,10,11,12,1):
            semester = 1
        else:
            semester = 2

        if user.rol_actual == 'coordinador':
            return qs.filter(
                year=now.year,
                cuatrimestre=semester
                )
        if user.rol_actual == 'mentor':
            return qs.filter(mentor=user,
                             year=now.year,
                             cuatrimestre=semester
                             )
        # mentorizado
        return qs.filter(mentorizado=user,
                         year=now.year,
                         cuatrimestre=semester
                         )

    def perform_create(self, serializer):
        # En create no se pasa year/cuatrimestre, queda auto en save()
        serializer.save()

    def get_permissions(self):
        if self.action == 'list':
            return [IsMentorOrMentorizadoOrCoordinador()]
        if self.action == 'create':
            return [IsCoordinador()]
        if self.action == 'retrieve':
            return [IsPairingOwnerOrCoordinador()]
        return [IsCoordinador()]
