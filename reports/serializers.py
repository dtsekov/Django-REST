from rest_framework import serializers
from .models import Informe

class InformeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Informe
        fields = '__all__'
        read_only_fields = ['id', 'user', 'emparejamiento', 'observaciones', 'created_at', 'updated_at', "fecha_entrega"]

    def validate(self, data):
        errors = {}
        tipo = data.get('tipo') if 'tipo' in data else (self.instance.tipo if self.instance else None)

        # Common required fields
        common_required = ['curso', 'grupo', 'nombre_completo', 'num_reuniones', 'temas_reuniones', 'horas_dedicadas', 'observaciones_generales']
        for f in common_required:
            if not data.get(f) and not (self.instance and getattr(self.instance, f)):
                errors[f] = 'Campo obligatorio.'

        # Seguimiento fields
        if tipo in [Informe.SEGUIMIENTO1, Informe.SEGUIMIENTO2]:
            role = (self.instance.user.rol_actual if self.instance else self.context['request'].user.rol_actual)

            if role == 'mentor':
                for f in ['participacion_mentorizada', 'problemas_detectados', 'mejoras_sugeridas', 'tipo_actividades']:
                    if not data.get(f) and not (self.instance and getattr(self.instance, f)):
                        errors[f] = 'Obligatorio para informe de seguimiento de mentor.'
            
            elif role == 'mentorizado':
                for f in ['actividades_realizadas', 'ayuda_recibida', 'mejoras_sugeridas', 'tipo_actividades']:
                    if not data.get(f) and not (self.instance and getattr(self.instance, f)):
                        errors[f] = 'Obligatorio para informe de seguimiento de mentorizado.'

        # Final fields based on role
        if tipo == Informe.FINAL:
            role = (self.instance.user.rol_actual if self.instance else self.context['request'].user.rol_actual)
            if role == 'mentor':
                for f in ['satisfaccion', 'recomendacion', 'ventajas_inconvenientes', 'mejoras_finales', 'labor_mentor',
                           'seguimiento', 'labor_positiva_integracion', 'mejora_implicacion', 'comunicacion', 'organizacion', 'beneficio_mentor']:
                    if not data.get(f) and not (self.instance and getattr(self.instance, f)):
                        errors[f] = 'Obligatorio para informe final de mentor.'
            elif role == 'mentorizado':
                for f in ['satisfaccion', 'recomendacion', 'ventajas_inconvenientes', 'mejoras_finales',
                           'labor_mentorizado', 'mejorar_organizacion', 'conocer_escuela', 'relaciones_personales',
                             'examenes', 'calificaciones', 'no_abandono', 'informacion', 'claridad_explicaciones', 'trato', 'facil_contacto', 'futuro_mentor', 'trabajo_mentor']:
                    if not data.get(f) and not (self.instance and getattr(self.instance, f)):
                        errors[f] = 'Obligatorio para informe final de mentorizado.'

        if errors:
            raise serializers.ValidationError(errors)
        return data