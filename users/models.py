## users/models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email debe ser proporcionado')
        email = self.normalize_email(email)
        # Forzar rol_actual por defecto a 'anonimo' si no se proporciona
        extra_fields.setdefault('rol_actual', 'anonimo')
        usuario = self.model(email=email, **extra_fields)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('rol_actual', 'coordinador')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('rol_actual') != 'coordinador':
            raise ValueError('Superuser must have rol_actual=coordinador')
        return self.create_user(email, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField('email address', unique=True)
    nombre = models.CharField(max_length=150)
    rol_actual = models.CharField(
        max_length=20,
        choices=[
            ('anonimo', 'Anónimo'),
            ('mentor', 'Mentor'),
            ('mentorizado', 'Mentorizado'),
            ('coordinador', 'Coordinador'),
        ],
        default='anonimo'
    )
    phone_validator = RegexValidator(
        regex=r'^(\+34)?[679]\d{8}$',
        message='El número debe ser un teléfono válido en España (opcional +34).'
    )
    phone_number = models.CharField(
        'phone number',
        max_length=12,
        validators=[phone_validator],
        blank=True,
        null=True
    )
    activo = models.BooleanField(default=True)
    fecha_activacion = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
