# users/serializers.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

Usuario = get_user_model()

class UsuarioSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = [
            'id', 'email', 'nombre', 'rol_actual',
            'phone_number', 'activo', 'fecha_activacion',
            'created_at', 'updated_at', 'password'
        ]
        # No permitir que rol_actual sea asignado en creación
        read_only_fields = ['id', 'activo', 'fecha_activacion', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['rol_actual'] = 'anonimo'
        password = validated_data.pop('password', None)
        usuario = Usuario.objects.create_user(
            email=validated_data.get('email'),
            password=password,
            nombre=validated_data.get('nombre'),
            phone_number=validated_data.get('phone_number')
        )
        return usuario
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        if 'rol_actual' in validated_data and request.user.rol_actual != 'coordinador':
            validated_data.pop('rol_actual')  # Solo coordinador puede cambiarlo
        return super().update(instance, validated_data)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    

    username_field = Usuario.USERNAME_FIELD

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'] = serializers.EmailField()
        self.fields['password'] = serializers.CharField()

   

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Añadimos claims personalizados:
        token['user_id'] = user.id
        token['rol_actual'] = user.rol_actual

        return token
