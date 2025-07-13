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
        "curso": "1",
        "grupo": "1",
        "nombre_completo": "Alonso Sáenz",
        "num_reuniones": 1,
        "temas_reuniones": "1",
        "horas_dedicadas": 0.1,
        "observaciones_generales": "1",
        "mejoras_sugeridas": "1",
        "tipo_actividades": "1",
        "problemas_detectados": "1",
        "participacion_mentorizada": "1",
        "actividades_realizadas": "",
        "ayuda_recibida": "",
        "satisfaccion": "",
        "recomendacion": "",
        "ventajas_inconvenientes": "",
        "mejoras_finales": "",
        "labor_mentor": "",
        "seguimiento": "",
        "labor_positiva_integracion": "",
        "mejora_implicacion": "",
        "comunicacion": "",
        "organizacion": "",
        "beneficio_mentor": "",
        "labor_mentorizado": "",
        "mejorar_organizacion": "",
        "conocer_escuela": "",
        "relaciones_personales": "",
        "examenes": "",
        "calificaciones": "",
        "no_abandono": "",
        "informacion": "",
        "claridad_explicaciones": "",
        "trato": "",
        "facil_contacto": "",
        "futuro_mentor": "",
        "trabajo_mentor": ""
}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_own_informe(self):
        informe = Informe.objects.create(
            tipo="seguimiento1", fecha_entrega=timezone.now(), curso="1",
            grupo="G1", nombre_completo="N", num_reuniones=1, temas_reuniones="T",
            tipo_actividades="A", participacion_mentorizada="P", mejoras_sugeridas="M",
            horas_dedicadas=1.0, user=self.mentor, emparejamiento=self.emparejamiento, observaciones_generales="Test", problemas_detectados="Test", 
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.get_token(self.mentor)}")
        url = reverse('reports-detail', args=[informe.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_reports_by_coordinador(self):
        Informe.objects.create(
            tipo="seguimiento1", fecha_entrega=timezone.now(), curso="1",
            grupo="G1", nombre_completo="N", num_reuniones=1, temas_reuniones="T",
            tipo_actividades="A", participacion_mentorizada="P", mejoras_sugeridas="M",
            horas_dedicadas=1.0, user=self.mentor, emparejamiento=self.emparejamiento, observaciones_generales="Test", problemas_detectados="Test", 
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.get_token(self.coordinador)}")
        response = self.client.get(reverse('reports-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_estado_by_coordinador(self):
        informe = Informe.objects.create(
            tipo="seguimiento1", fecha_entrega=timezone.now(), curso="1",
            grupo="G1", nombre_completo="N", num_reuniones=1, temas_reuniones="T",
            tipo_actividades="A", participacion_mentorizada="P", mejoras_sugeridas="M",
            horas_dedicadas=1.0, user=self.mentor, emparejamiento=self.emparejamiento, observaciones_generales="Test", problemas_detectados="Test", 
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.get_token(self.coordinador)}")
        url = reverse('reports-detail', args=[informe.id])
        response = self.client.patch(url, {"estado": "aprobado", "observaciones": "OK"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['estado'], "aprobado")

    def test_patch_estado_by_non_coordinador_forbidden(self):
        informe = Informe.objects.create(
            tipo="seguimiento1", fecha_entrega=timezone.now(), curso="1",
            grupo="G1", nombre_completo="N", num_reuniones=1, temas_reuniones="T",
            tipo_actividades="A", participacion_mentorizada="P", mejoras_sugeridas="M",
            horas_dedicadas=1.0, user=self.mentor, emparejamiento=self.emparejamiento, observaciones_generales="Test", problemas_detectados="Test", 
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.get_token(self.mentor)}")
        url = reverse('reports-detail', args=[informe.id])
        response = self.client.patch(url, {"estado": "aprobado"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)