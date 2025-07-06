from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'usuario', 'mensaje', 'tipo', 'fecha_envio', 'leida', 'created_at', 'updated_at']
        read_only_fields = ['id','fecha_envio', 'created_at', 'updated_at']

    def update(self, instance, validated_data):
        # Permitir sólo actualizar el campo 'leida'
        instance.leida = validated_data.get('leida', instance.leida)
        instance.save()
        return instance