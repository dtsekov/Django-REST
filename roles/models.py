from django.db import models
from django.conf import settings
from django.utils import timezone

class SolicitudRol(models.Model):
    CUATRIMESTRE_CHOICES = [
        (1, 'Primer cuatrimestre'),
        (2, 'Segundo cuatrimestre'),
    ]
    TIPO_CHOICES = [
        ('mentor', 'Mentor'),
        ('mentorizado', 'Mentorizado'),
    ]
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aceptada', 'Aceptada'),
        ('rechazada', 'Rechazada'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='solicitudes_rol'
    )
    year = models.IntegerField()
    cuatrimestre = models.IntegerField(choices=CUATRIMESTRE_CHOICES)
    tipo = models.CharField(max_length=12, choices=TIPO_CHOICES)
    fecha_envio = models.DateTimeField(auto_now_add=True)
    contenido = models.TextField()
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')
    comentario_coordinador = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Asignar year y cuatrimestre automáticamente si no están definidos
        now = timezone.now()
        if not self.year:
            self.year = now.year
        if not self.cuatrimestre:
            month = now.month
            self.cuatrimestre = 1 if month in (9, 10, 11, 12, 1) else 2
        super().save(*args, **kwargs)

    def __str__(self):
        return f"SolicitudRol {self.id} - {self.usuario.email} ({self.tipo})"

