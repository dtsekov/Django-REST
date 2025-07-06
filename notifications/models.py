from django.db import models
from django.conf import settings

class Notification(models.Model):
    TIPO_CHOICES = [
        ('info', 'Info'),
        ('alerta', 'Alerta'),
        ('error', 'Error'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    mensaje = models.TextField()
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    fecha_envio = models.DateTimeField(auto_now_add=True)
    leida = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Notification {self.id} to {self.usuario.email}"
