from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import Usuario
from rest_framework_simplejwt.tokens import RefreshToken
from roles.models import SolicitudRol


def get_token(user):
    return str(RefreshToken.for_user(user).access_token)


class RolesTests(APITestCase):
    def setUp(self):
        self.coordinador = Usuario.objects.create_user(email="coord@test.com", password="Test1234!", rol_actual="coordinador")
        self.anonimo = Usuario.objects.create_user(email="anon@test.com", password="Test1234!", rol_actual="anonimo")

    def test_create_solicitud_rol(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token(self.anonimo)}")
        data = {
            "tipo": "mentor",
            "contenido": "Me gustaría ser mentor."
        }
        response = self.client.post(reverse("roles-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['estado'], 'pendiente')

    def test_list_solicitudes_by_coordinador(self):
        SolicitudRol.objects.create(usuario=self.anonimo, tipo="mentor", contenido="Motivación")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token(self.coordinador)}")
        response = self.client.get(reverse("roles-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_patch_solicitud_estado_by_coordinador(self):
        solicitud = SolicitudRol.objects.create(usuario=self.anonimo, tipo="mentorizado", contenido="...")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token(self.coordinador)}")
        url = reverse("roles-detail", args=[solicitud.id])
        response = self.client.patch(url, {"estado": "aceptada", "comentario_coordinador": "Aprobado"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['estado'], "aceptada")

    def test_retrieve_solicitud_by_owner(self):
        solicitud = SolicitudRol.objects.create(usuario=self.anonimo, tipo="mentor", contenido="Motivación")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token(self.anonimo)}")
        url = reverse("roles-detail", args=[solicitud.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['usuario'], self.anonimo.id)
