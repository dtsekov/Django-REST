from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import Usuario
from rest_framework_simplejwt.tokens import RefreshToken
from notifications.models import Notification


def get_token(user):
    return str(RefreshToken.for_user(user).access_token)


class NotificationsTests(APITestCase):
    def setUp(self):
        self.coordinador = Usuario.objects.create_user(email="coord@test.com", password="Test1234!", rol_actual="coordinador")
        self.anonimo = Usuario.objects.create_user(email="anon@test.com", password="Test1234!", rol_actual="anonimo")

    def test_create_notification_by_coordinador(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token(self.coordinador)}")
        data = {
            "usuario": self.anonimo.id,
            "mensaje": "Tu solicitud fue aceptada",
            "tipo": "info"
        }
        response = self.client.post(reverse("notifications-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['leida'], False)

    def test_patch_notification_leida(self):
        notification = Notification.objects.create(usuario=self.anonimo, mensaje="Aviso", tipo="alerta")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token(self.anonimo)}")
        url = reverse("notifications-detail", args=[notification.id])
        response = self.client.patch(url, {"leida": True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['leida'])

    def test_create_notification_denied_for_non_coordinador(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token(self.anonimo)}")
        data = {
            "usuario": self.anonimo.id,
            "mensaje": "Intento no válido",
            "tipo": "info"
        }
        response = self.client.post(reverse("notifications-list"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_notifications_returns_only_user_notifications(self):
        Notification.objects.create(usuario=self.anonimo, mensaje="Tu informe ha sido revisado", tipo="info")
        Notification.objects.create(usuario=self.coordinador, mensaje="Nueva solicitud recibida", tipo="alerta")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token(self.anonimo)}")
        response = self.client.get(reverse("notifications-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for notif in response.data:
            self.assertEqual(notif['usuario'], self.anonimo.id)