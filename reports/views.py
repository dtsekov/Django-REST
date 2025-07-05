from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from pairings.models import Emparejamiento
from .models import Informe
from .serializers import InformeSerializer
from users.permissions import IsCoordinador, IsOwnerOrCoordinador, IsMentorOrMentorizado
from django.utils import timezone

class InformeViewSet(viewsets.ModelViewSet):
    queryset = Informe.objects.all()
    serializer_class = InformeSerializer

    def _current_year_semester(self):
        now = timezone.now()
        year = now.year
        month = now.month
        # 
        semester = 1 if month >= 9 or month == 1 else 2
        return year, semester

    def perform_create(self, serializer):
        user = self.request.user
        year, semester = self._current_year_semester()
        # Determine emparejamiento: mentors may have multiple, mentorizados one
        if user.rol_actual == 'mentor':
            pairing = Emparejamiento.objects.filter(
                mentor=user,
                fecha_emparejamiento__year=year,
                cuatrimestre=semester
            ).first()
        else:  # mentorizado
            pairing = Emparejamiento.objects.get(
                mentorizado=user,
                fecha_emparejamiento__year=year,
                cuatrimestre=semester
            )
        serializer.save(
            respuesta_general=user,
            estado=Informe.PENDIENTE,
            emparejamiento=pairing
        )
    
    def get_queryset(self):
        user = self.request.user
        year, semester = self._current_year_semester()
        # Coordinator sees all for current year and semester via emparejamiento
        if user.rol_actual == 'coordinador':
            return super().get_queryset().filter(
                emparejamiento__fecha_emparejamiento__year=year,
                emparejamiento__cuatrimestre=semester
            )
        # 
        if user.rol_actual == 'mentor':
            return super().get_queryset().filter(
            respuesta_general=user,
            emparejamiento__fecha_emparejamiento__year=year,
            emparejamiento__cuatrimestre=semester
            )
        # 
        return super().get_queryset().filter(
            respuesta_general=user,
            emparejamiento__fecha_emparejamiento__year=year,
            emparejamiento__cuatrimestre=semester
        )


    def get_permissions(self):
        if self.action in ['list', 'create']:
            return [IsMentorOrMentorizado() or IsCoordinador()]
        if self.action == 'retrieve':
            return [IsOwnerOrCoordinador()]
        if self.action == 'partial_update':
            return [IsCoordinador()]
        return [IsCoordinador()]