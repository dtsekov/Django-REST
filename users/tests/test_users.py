from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import Usuario
from rest_framework_simplejwt.tokens import RefreshToken


def get_token(user):
    return str(RefreshToken.for_user(user).access_token)


class UsuarioTests(APITestCase):
    def setUp(self):
        self.coordinador = Usuario.objects.create_user(email="coord@test.com", password="Test1234!", rol_actual="coordinador")
        self.mentor = Usuario.objects.create_user(email="mentor@test.com", password="Test1234!", rol_actual="mentor")
        self.anonimo = Usuario.objects.create_user(email="anon@test.com", password="Test1234!", rol_actual="anonimo")

    def test_create_usuario(self):
        response = self.client.post(reverse('usuario-list'), {
            "email": "nuevo@test.com",
            "password": "Test1234!",
            "nombre": "Nuevo Usuario",
            "phone_number": "600000000"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['rol_actual'], 'anonimo')

    def test_login_jwt(self):
        response = self.client.post(reverse('token_obtain_pair'), {"email": "mentor@test.com", "password": "Test1234!"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_get_users_list_by_coordinador(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token(self.coordinador)}")
        response = self.client.get(reverse('usuario-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_users_list_by_mentor_fails(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token(self.mentor)}")
        response = self.client.get(reverse('usuario-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_users_list_by_anonimo_fails(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token(self.anonimo)}")
        response = self.client.get(reverse('usuario-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_own_profile(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token(self.mentor)}")
        url = reverse('usuario-detail', args=[self.mentor.id])
        response = self.client.patch(url, {"nombre": "Cambiado"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], "Cambiado")

    def test_patch_rol_actual_by_user_forbidden(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token(self.mentor)}")
        url = reverse('usuario-detail', args=[self.mentor.id])
        response = self.client.patch(url, {"rol_actual": "coordinador"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['rol_actual'], "mentor")  # No cambio

    def test_patch_rol_actual_by_coordinador(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token(self.coordinador)}")
        url = reverse('usuario-detail', args=[self.anonimo.id])
        response = self.client.patch(url, {"rol_actual": "mentor"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['rol_actual'], "mentor")

    def test_retrieve_by_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token(self.mentor)}")
        url = reverse('usuario-detail', args=[self.mentor.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_by_other_user_forbidden(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token(self.anonimo)}")
        url = reverse('usuario-detail', args=[self.mentor.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_by_coordinador_allowed(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token(self.coordinador)}")
        url = reverse('usuario-detail', args=[self.mentor.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)