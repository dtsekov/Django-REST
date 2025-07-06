from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import Usuario
from pairings.models import Emparejamiento
from reports.models import Informe
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone

class InformeTests(APITestCase):
    def setUp(self):
        self.coordinador = Usuario.objects.create_user(email="coord@test.com", password="Test1234!", rol_actual="coordinador")
        self.mentor = Usuario.objects.create_user(email="mentor@test.com", password="Test1234!", rol_actual="mentor")
        self.mentorizado = Usuario.objects.create_user(email="ment@test.com", password="Test1234!", rol_actual="mentorizado")
        # Crear emparejamiento actual
        self.emparejamiento = Emparejamiento.objects.create(mentor=self.mentor, mentorizado=self.mentorizado)

    def get_token(self, user):
        return str(RefreshToken.for_user(user).access_token)

    def test_create_informe_seguimiento_by_mentor(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.get_token(self.mentor)}")
        url = reverse('reports-list')
        data = {
            "tipo": "seguimiento1",
            "contenido": "Texto",
            "fecha_entrega": timezone.now().isoformat(),
            "curso": "1",
            "grupo": "G1",
            "nombre_completo": "Nombre",
            "num_reuniones": 2,
            "temas_reuniones": "Temas",
            "tipo_actividades": "Act",
            "participacion_mentorizada": "Part",
            "mejoras_sugeridas": "Mejoras",
            "horas_dedicadas": "2.5"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_own_informe(self):
        informe = Informe.objects.create(
            tipo="seguimiento1", contenido="t", fecha_entrega=timezone.now(), curso="1",
            grupo="G1", nombre_completo="N", num_reuniones=1, temas_reuniones="T",
            tipo_actividades="A", participacion_mentorizada="P", mejoras_sugeridas="M",
            horas_dedicadas=1.0, user=self.mentor, emparejamiento=self.emparejamiento
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.get_token(self.mentor)}")
        url = reverse('reports-detail', args=[informe.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_reports_by_coordinador(self):
        Informe.objects.create(
            tipo="seguimiento1", contenido="t", fecha_entrega=timezone.now(), curso="1",
            grupo="G1", nombre_completo="N", num_reuniones=1, temas_reuniones="T",
            tipo_actividades="A", participacion_mentorizada="P", mejoras_sugeridas="M",
            horas_dedicadas=1.0, user=self.mentor, emparejamiento=self.emparejamiento
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.get_token(self.coordinador)}")
        response = self.client.get(reverse('reports-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_estado_by_coordinador(self):
        informe = Informe.objects.create(
            tipo="seguimiento1", contenido="t", fecha_entrega=timezone.now(), curso="1",
            grupo="G1", nombre_completo="N", num_reuniones=1, temas_reuniones="T",
            tipo_actividades="A", participacion_mentorizada="P", mejoras_sugeridas="M",
            horas_dedicadas=1.0, user=self.mentor, emparejamiento=self.emparejamiento
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.get_token(self.coordinador)}")
        url = reverse('reports-detail', args=[informe.id])
        response = self.client.patch(url, {"estado": "aprobado", "observaciones": "OK"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['estado'], "aprobado")

    def test_patch_estado_by_non_coordinador_forbidden(self):
        informe = Informe.objects.create(
            tipo="seguimiento1", contenido="t", fecha_entrega=timezone.now(), curso="1",
            grupo="G1", nombre_completo="N", num_reuniones=1, temas_reuniones="T",
            tipo_actividades="A", participacion_mentorizada="P", mejoras_sugeridas="M",
            horas_dedicadas=1.0, user=self.mentor, emparejamiento=self.emparejamiento
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.get_token(self.mentor)}")
        url = reverse('reports-detail', args=[informe.id])
        response = self.client.patch(url, {"estado": "aprobado"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)