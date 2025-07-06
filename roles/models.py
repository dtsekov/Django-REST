from django.db import models
from django.conf import settings

class SolicitudRol(models.Model):
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
    tipo = models.CharField(max_length=12, choices=TIPO_CHOICES)
    fecha_envio = models.DateTimeField(auto_now_add=True)
    contenido = models.TextField()
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')
    comentario_coordinador = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"SolicitudRol {self.id} - {self.usuario.email} ({self.tipo})"

