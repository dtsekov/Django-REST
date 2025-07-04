from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer
from rest_framework import viewsets
from .models import Usuario
from .serializers import UsuarioSerializer
from .permissions import IsOwnerOrCoordinador, IsCoordinador
from rest_framework.permissions import AllowAny

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        if self.action == 'list':
            return [IsCoordinador()]
        if self.action in ('retrieve', 'partial_update'):
            return [IsOwnerOrCoordinador()]
        # Fallback: solo coordinador
        return [IsCoordinador()]