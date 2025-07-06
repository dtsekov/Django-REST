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
    contenido = models.TextField()
    fecha_entrega = models.DateTimeField(default=timezone.now)
    curso = models.CharField(max_length=1)
    grupo = models.CharField(max_length=15, blank=True)
    nombre_completo = models.CharField(max_length=150)
    num_reuniones = models.IntegerField()
    temas_reuniones = models.TextField()
    tipo_actividades = models.TextField()
    participacion_mentorizada = models.TextField()
    mejoras_sugeridas = models.TextField()
    horas_dedicadas = models.DecimalField(max_digits=5, decimal_places=2)
    observaciones_generales = models.TextField(blank=True)
    labor_mentor = models.TextField(blank=True)
    ventajas_inconvenientes = models.TextField(blank=True)
    mejoras_finales = models.TextField(blank=True)
    labor_mentorizado = models.TextField(blank=True)
    experiencia_informada = models.TextField(blank=True)
    satisfaccion = models.TextField(blank=True)
    recomendacion = models.TextField(blank=True)
    estado = models.CharField(
        max_length=10, choices=ESTADO_CHOICES, default=PENDIENTE
    )
    observaciones = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Informe {self.id} - {self.tipo}"
