from django.db import models
from django.conf import settings
from django.utils import timezone

class Informe(models.Model):
    # Choices for type of report
    SEGUIMIENTO1 = 'seguimiento1'
    SEGUIMIENTO2 = 'seguimiento2'
    FINAL = 'final'
    TIPO_CHOICES = [
        (SEGUIMIENTO1, 'Seguimiento 1'),
        (SEGUIMIENTO2, 'Seguimiento 2'),
        (FINAL,        'Final'),
    ]

    # Choices for status
    PENDIENTE = 'pendiente'
    APROBADO = 'aprobado'
    DEVUELTO = 'devuelto'
    ESTADO_CHOICES = [
        (PENDIENTE, 'Pendiente'),
        (APROBADO,  'Aprobado'),
        (DEVUELTO,  'Devuelto'),
    ]

    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='informes'
    )
    emparejamiento = models.ForeignKey(
        'pairings.Emparejamiento',
        on_delete=models.CASCADE,
        related_name='informes'
    )

    fecha_entrega = models.DateTimeField(default=timezone.now)

    # Common fields (both roles)
    curso = models.CharField(max_length=1)  # Mentor/Mentorizado
    grupo = models.CharField(max_length=15, blank=True)  # Mentor/Mentorizado
    nombre_completo = models.CharField(max_length=150)  # Mentor/Mentorizado
    num_reuniones = models.IntegerField()  # Mentor/Mentorizado
    temas_reuniones = models.TextField()  # Mentor/Mentorizado
    horas_dedicadas = models.DecimalField(max_digits=5, decimal_places=2)  # Mentor/Mentorizado
    satisfaccion = models.TextField(blank=True)  # Final Mentor/Final Mentorizado
    recomendacion = models.TextField(blank=True)  # Final Mentor/Final Mentorizado
    tipo_actividades = models.TextField(blank=True)  # Mentor/Mentorizado solo en seguimiento
    observaciones_generales = models.TextField(blank=True)  # Mentor/Mentorizado
    mejoras_sugeridas = models.TextField(blank=True)  # Mentor/Mentorizado

    # Mentor-only (Seguimiento)
    problemas_detectados = models.TextField(blank=True)  # Mentor only
    participacion_mentorizada = models.TextField(blank=True)  # Mentor only
    
    

    # Final Mentor
    labor_mentor = models.TextField(blank=True)  # Mentor only
    seguimiento = models.TextField(blank=True)  # Mentor only
    labor_positiva_integracion = models.TextField(blank=True)  # Mentor only
    mejora_implicacion = models.TextField(blank=True)  # Mentor only
    comunicacion = models.TextField(blank=True)  # Mentor only
    organizacion = models.TextField(blank=True)  # Mentor only
    beneficio_mentor = models.TextField(blank=True)  # Mentor only

    # Shared final observations
    ventajas_inconvenientes = models.TextField(blank=True)  # Both roles
    mejoras_finales = models.TextField(blank=True)  # Both roles

    # Mentorizado-only (Seguimiento)
    actividades_realizadas = models.TextField(blank=True)  # Mentorizado only
    ayuda_recibida = models.TextField(blank=True)  # Mentorizado only

    # Final Mentorizado
    labor_mentorizado = models.TextField(blank=True)  # Mentorizado only
    mejorar_organizacion = models.TextField(blank=True)  # Mentorizado only
    conocer_escuela = models.TextField(blank=True)  # Mentorizado only
    relaciones_personales = models.TextField(blank=True)  # Mentorizado only
    examenes = models.TextField(blank=True)  # Mentorizado only
    calificaciones = models.TextField(blank=True)  # Mentorizado only
    no_abandono = models.TextField(blank=True)  # Mentorizado only
    informacion = models.TextField(blank=True)  # Mentorizado only
    claridad_explicaciones = models.TextField(blank=True)  # Mentorizado only
    trato = models.TextField(blank=True)  # Mentorizado only
    facil_contacto = models.TextField(blank=True)  # Mentorizado only
    futuro_mentor = models.TextField(blank=True)  # Mentorizado only
    trabajo_mentor = models.TextField(blank=True)  # Mentorizado only

    estado = models.CharField(
        max_length=10, choices=ESTADO_CHOICES, default=PENDIENTE
    )
    observaciones = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Informe {self.id} - {self.tipo}"