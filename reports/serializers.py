from rest_framework import serializers
from .models import Informe

class InformeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Informe
        fields = '__all__'
        read_only_fields = ['id', 'respuesta_general', 'emparejamiento', 'observaciones', 'created_at', 'updated_at', "fecha_entrega"]

    def validate(self, data):
        errors = {}
        tipo = data.get('tipo') if 'tipo' in data else (self.instance.tipo if self.instance else None)

        # Common required fields
        common_required = ['contenido', 'curso', 'nombre_completo', 'num_reuniones']
        for f in common_required:
            if not data.get(f) and not (self.instance and getattr(self.instance, f)):
                errors[f] = 'Campo obligatorio.'

        # Seguimiento fields
        if tipo in [Informe.SEGUIMIENTO1, Informe.SEGUIMIENTO2]:
            for f in ['temas_reuniones', 'tipo_actividades', 'participacion_mentorizada', 'mejoras_sugeridas', 'horas_dedicadas']:
                if not data.get(f) and not (self.instance and getattr(self.instance, f)):
                    errors[f] = 'Obligatorio para informe de seguimiento.'

        # Final fields based on role
        if tipo == Informe.FINAL:
            role = (self.instance.respuesta_general.rol_actual if self.instance else self.context['request'].user.rol_actual)
            if role == 'mentor':
                for f in ['labor_mentor', 'ventajas_inconvenientes', 'mejoras_finales']:
                    if not data.get(f) and not (self.instance and getattr(self.instance, f)):
                        errors[f] = 'Obligatorio para informe final de mentor.'
            elif role == 'mentorizado':
                for f in ['labor_mentorizado', 'experiencia_informada', 'satisfaccion', 'recomendacion']:
                    if not data.get(f) and not (self.instance and getattr(self.instance, f)):
                        errors[f] = 'Obligatorio para informe final de mentorizado.'

        if errors:
            raise serializers.ValidationError(errors)
        return data