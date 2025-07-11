from rest_framework import serializers
from .models import SolicitudRol

class SolicitudRolSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolicitudRol
        fields = ['id', 'usuario', 'tipo', 'fecha_envio', 'contenido', 'estado', 'comentario_coordinador', 'created_at', 'updated_at']
        read_only_fields = ['id', 'usuario', 'fecha_envio', 'created_at', 'updated_at', 'year', 'cuatrimestre']

    def create(self, validated_data):
        # Asignar usuario actual y estado pendiente
        user = self.context['request'].user
        return SolicitudRol.objects.create(usuario=user, estado='pendiente', **validated_data)