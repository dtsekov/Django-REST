from rest_framework import serializers
from .models import Emparejamiento
from django.utils import timezone

class EmparejamientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emparejamiento
        fields = ['id', 'mentor', 'mentorizado', 'year', 'cuatrimestre', 'fecha_emparejamiento', 'comentarios', 'created_at', 'updated_at']
        read_only_fields = ['id', 'year', 'cuatrimestre', 'fecha_emparejamiento', 'created_at', 'updated_at']

    def validate(self, data):
        mentorizado = data.get('mentorizado', None)
        # Determinar año y cuatrimestre actual
        now = timezone.now()
        year = now.year
        month = now.month
        cuatri = 1 if month in (9, 10, 11, 12, 1) else 2
        # Verificar existencia de emparejamiento previo
        if Emparejamiento.objects.filter(mentorizado=mentorizado, year=year, cuatrimestre=cuatri).exists():
            raise serializers.ValidationError({'mentorizado': 'Ya tiene un emparejamiento en este año y cuatrimestre.'})
        return data