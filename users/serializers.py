# users/serializers.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)


        # Añadimos claims personalizados:
        token['user_id'] = user.id

      
        token['rol_actual'] = user.rol_actual

        return token
