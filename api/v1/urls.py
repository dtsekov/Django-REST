from django.urls import path
from users.views import MyTokenObtainPairView
from rest_framework.routers import DefaultRouter
from users.views import UsuarioViewSet

router = DefaultRouter()
router.register(r'users', UsuarioViewSet, basename='usuario')


urlpatterns = [
    path('auth/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
] + router.urls
