from django.db import models
from django.conf import settings
from django.utils import timezone

class Emparejamiento(models.Model):
    CUATRIMESTRE_CHOICES = [
        (1, 'Primer cuatrimestre'),
        (2, 'Segundo cuatrimestre'),
    ]

    mentor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='emparejamientos_mentor'
    )
    mentorizado = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='emparejamientos_mentorizado'
    )
    year = models.IntegerField()
    cuatrimestre = models.IntegerField(choices=CUATRIMESTRE_CHOICES)
    fecha_emparejamiento = models.DateTimeField(auto_now_add=True)
    comentarios = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('mentorizado', 'year', 'cuatrimestre')  # un mentorizado solo uno por año/cuatrimestre

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
        return f"{self.mentor.email} → {self.mentorizado.email} ({self.year}T{self.cuatrimestre})"