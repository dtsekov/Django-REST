from django.urls import include, path
from pairings.views import EmparejamientoViewSet
from users.views import MyTokenObtainPairView
from rest_framework.routers import DefaultRouter
from users.views import UsuarioViewSet
from reports.views import InformeViewSet
from roles.views import SolicitudRolViewSet
from notifications.views import NotificationViewSet
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

router = DefaultRouter()
router.register(r'users', UsuarioViewSet, basename='usuario')
router.register(r'reports', InformeViewSet, basename='reports')
router.register(r'pairings', EmparejamientoViewSet, basename='pairings')
router.register(r'roles', SolicitudRolViewSet, basename='roles')
router.register(r'notifications', NotificationViewSet, basename='notifications')

urlpatterns = [
    path('auth/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/password/reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

] + router.urls
