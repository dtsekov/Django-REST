from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import Usuario
from pairings.models import Emparejamiento
from rest_framework_simplejwt.tokens import RefreshToken

class EmparejamientoTests(APITestCase):
    def setUp(self):
        self.coordinador = Usuario.objects.create_user(email="coord@test.com", password="Test1234!", rol_actual="coordinador")
        self.mentor = Usuario.objects.create_user(email="mentor@test.com", password="Test1234!", rol_actual="mentor")
        self.mentorizado = Usuario.objects.create_user(email="ment@test.com", password="Test1234!", rol_actual="mentorizado")

    def get_token(self, user):
        return str(RefreshToken.for_user(user).access_token)

    def test_create_pairing_by_coordinador(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.get_token(self.coordinador)}")
        data = {"mentor": self.mentor.id, "mentorizado": self.mentorizado.id}
        response = self.client.post(reverse('pairings-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_pairing_by_non_coordinador_forbidden(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.get_token(self.mentor)}")
        data = {"mentor": self.mentor.id, "mentorizado": self.mentorizado.id}
        response = self.client.post(reverse('pairings-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unique_pairing_constraint(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.get_token(self.coordinador)}")
        # Primer emparejamiento
        self.client.post(reverse('pairings-list'), {"mentor": self.mentor.id, "mentorizado": self.mentorizado.id})
        # Segundo en mismo cuatrimestre y año
        response = self.client.post(reverse('pairings-list'), {"mentor": self.mentor.id, "mentorizado": self.mentorizado.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_pairings_coordinador(self):
        Emparejamiento.objects.create(mentor=self.mentor, mentorizado=self.mentorizado)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.get_token(self.coordinador)}")
        response = self.client.get(reverse('pairings-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_list_pairings_by_mentor(self):
        Emparejamiento.objects.create(mentor=self.mentor, mentorizado=self.mentorizado)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.get_token(self.mentor)}")
        response = self.client.get(reverse('pairings-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(item['mentor'] == self.mentor.id for item in response.data))

    def test_list_pairings_by_mentorizado(self):
        Emparejamiento.objects.create(mentor=self.mentor, mentorizado=self.mentorizado)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.get_token(self.mentorizado)}")
        response = self.client.get(reverse('pairings-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(item['mentorizado'] == self.mentorizado.id for item in response.data))