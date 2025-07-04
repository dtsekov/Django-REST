# users/serializers.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

Usuario = get_user_model()

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            'id', 'email', 'nombre', 'rol_actual',
            'phone_number', 'activo', 'fecha_activacion',
            'created_at', 'updated_at'
        ]
        # No permitir que rol_actual sea asignado en creación
        read_only_fields = ['id', 'rol_actual', 'activo', 'fecha_activacion', 'created_at', 'updated_at']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        usuario = Usuario.objects.create_user(
            email=validated_data.get('email'),
            password=password,
            nombre=validated_data.get('nombre'),
            phone_number=validated_data.get('phone_number')
        )
        return usuario

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = Usuario.USERNAME_FIELD

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Rename 'username' field to 'email'
        if 'username' in self.fields:
            self.fields['email'] = self.fields.pop('username')

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Añadimos claims personalizados:
        token['user_id'] = user.id
        token['rol_actual'] = user.rol_actual

        return token
