from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from appointments.models import Appointments
from health_professionals.models import HealthProfessional
from datetime import date
from rest_framework_simplejwt.tokens import RefreshToken


class AppointmentsCRUDTest(APITestCase):

    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.professional = HealthProfessional.objects.create(
            social_name='Dra. Maria Santos',
            profession='Psicóloga',
            address='Av. Paulista, 1000',
            contact='11988888888'
        )
        
        self.list_create_url = '/api/v1/appointments/'
    
    def get_detail_url(self, pk):
        return f'/api/v1/appointments/{pk}/'

    
    def test_create_appointment_success(self):
        data = {
            'date': '2025-12-30',
            'health_professional': self.professional.id
        }
        response = self.client.post(self.list_create_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Appointments.objects.count(), 1)
        self.assertEqual(response.data['date'], '2025-12-30')
    
    def test_create_appointment_missing_fields(self):
        """Testa criar consulta sem campos obrigatórios"""
        # Sem data
        response = self.client.post(
            self.list_create_url,
            {'health_professional': self.professional.id},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('date', response.data)
        
        # Sem profissional
        response = self.client.post(
            self.list_create_url,
            {'date': '2025-12-30'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('health_professional', response.data)
    
    def test_create_appointment_invalid_data(self):
        """Testa criar consulta com dados inválidos"""
        # Data em formato errado
        response = self.client.post(
            self.list_create_url,  
            {
                'date': '30/12/2025',
                'health_professional': self.professional.id
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Profissional inexistente
        response = self.client.post(
            self.list_create_url,
            {
                'date': '2025-12-30',
                'health_professional': 99999
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_appointment_without_authentication(self):
        """Testa criar consulta sem autenticação"""
        self.client.credentials()  # Remove token
        
        data = {
            'date': '2025-12-30',
            'health_professional': self.professional.id
        }
        response = self.client.post(self.list_create_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_list_appointments(self):
        """Testa listar todas as consultas"""
        # Cria 3 consultas
        Appointments.objects.create(date=date(2025, 12, 25), health_professional=self.professional)
        Appointments.objects.create(date=date(2025, 12, 26), health_professional=self.professional)
        Appointments.objects.create(date=date(2025, 12, 27), health_professional=self.professional)
        
        response = self.client.get(self.list_create_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
    
    def test_list_appointments_empty(self):
        """Testa listar quando não há consultas"""
        response = self.client.get(self.list_create_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
    
    def test_retrieve_appointment(self):
        """Testa buscar uma consulta específica"""
        appointment = Appointments.objects.create(
            date=date(2025, 12, 25),
            health_professional=self.professional
        )
        
        response = self.client.get(self.get_detail_url(appointment.id))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], appointment.id)
        self.assertEqual(response.data['date'], '2025-12-25')
    
    def test_retrieve_appointment_not_found(self):
        """Testa buscar consulta inexistente"""
        response = self.client.get(self.get_detail_url(99999))
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    
    def test_update_appointment_put(self):
        """Testa atualizar consulta completamente (PUT)"""
        appointment = Appointments.objects.create(
            date=date(2025, 12, 25),
            health_professional=self.professional
        )
        
        data = {
            'date': '2025-12-31',
            'health_professional': self.professional.id
        }
        response = self.client.put(self.get_detail_url(appointment.id), data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        appointment.refresh_from_db()
        self.assertEqual(appointment.date, date(2025, 12, 31))
    
    def test_update_appointment_patch(self):
        """Testa atualizar parcialmente (PATCH)"""
        appointment = Appointments.objects.create(
            date=date(2025, 12, 25),
            health_professional=self.professional
        )
        
        response = self.client.patch(
            self.get_detail_url(appointment.id),
            {'date': '2025-12-28'},
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        appointment.refresh_from_db()
        self.assertEqual(appointment.date, date(2025, 12, 28))
    
    def test_update_appointment_not_found(self):
        """Testa atualizar consulta inexistente"""
        response = self.client.patch(
            self.get_detail_url(99999),
            {'date': '2025-12-31'},
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    
    def test_delete_appointment(self):
        """Testa deletar consulta"""
        appointment = Appointments.objects.create(
            date=date(2025, 12, 25),
            health_professional=self.professional
        )
        
        self.assertEqual(Appointments.objects.count(), 1)
        
        response = self.client.delete(self.get_detail_url(appointment.id))
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Appointments.objects.count(), 0)
    
    def test_delete_appointment_not_found(self):
        """Testa deletar consulta inexistente"""
        response = self.client.delete(self.get_detail_url(99999))
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    
    def test_filter_by_professional(self):
        """Testa buscar consultas por profissional específico"""
        # Cria outro profissional
        other_professional = HealthProfessional.objects.create(
            social_name='Dr. Pedro Souza',
            profession='Dentista',
            address='Rua B, 456',
            contact='11977777777'
        )
        
        # Cria consultas para ambos
        Appointments.objects.create(date=date(2025, 12, 25), health_professional=self.professional)
        Appointments.objects.create(date=date(2025, 12, 26), health_professional=self.professional)
        Appointments.objects.create(date=date(2025, 12, 27), health_professional=other_professional)
        
        # Filtra pelo primeiro profissional
        url = f'{self.list_create_url}?health_professional={self.professional.id}'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # Verifica se todas são do profissional correto
        for appointment in response.data:
            self.assertEqual(appointment['health_professional'], self.professional.id)
