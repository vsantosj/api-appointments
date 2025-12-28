from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from datetime import date, timedelta
from health_professionals.models import HealthProfessional
from appointments.models import Appointments


class AppointmentsTestCase(APITestCase):

    def setUp(self):
        self.normal_user = User.objects.create_user(
            username='userTest', 
            password='userPass'
        )

        self.health_professional = HealthProfessional.objects.create(
            social_name='Dra. Ana Silva',
            profession='Psicóloga',
            address='Rua das Flores, 123',
            contact='(11) 99999-9999'
        )
        
        self.future_date = date.today() + timedelta(days=5)
        self.appointment = Appointments.objects.create(
            date=self.future_date,
            health_professional=self.health_professional
        )
        
        self.url = reverse('appointments-detail-view', kwargs={'pk': self.appointment.pk})
        self.list_url = reverse('appointments-create-list')

    # TEST CREATE
    
    def test_create_appointment_success(self):
        self.client.force_authenticate(user=self.normal_user)
        data = {
            "date": str(date.today() + timedelta(days=10)),
            "health_professional": self.health_professional.id
        }
        
        response = self.client.post(self.list_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['health_professional'], self.health_professional.id)
        self.assertEqual(Appointments.objects.count(), 2)
    
    def test_create_appointment_with_missing_fields(self):
        self.client.force_authenticate(user=self.normal_user)
        
        data = {
            "date": str(date.today() + timedelta(days=10))
        }
        
        response = self.client.post(self.list_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('health_professional', response.data)
    
    def test_create_appointment_with_past_date(self):
        self.client.force_authenticate(user=self.normal_user)
        
        past_date = date.today() - timedelta(days=5)
        data = {
            "date": str(past_date),
            "health_professional": self.health_professional.id
        }
        
        response = self.client.post(self.list_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_duplicate_appointment(self):
        self.client.force_authenticate(user=self.normal_user)
        
        data = {
            "date": str(self.future_date),
            "health_professional": self.health_professional.id
        }
        
        response = self.client.post(self.list_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # TEST GET
    
    def test_list_appointments_success(self):
        #Teste de listagem de agendamentos
        self.client.force_authenticate(user=self.normal_user)
        
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_get_appointment_by_id_success(self):
        self.client.force_authenticate(user=self.normal_user)
        
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.appointment.id)
        self.assertEqual(response.data['date'], str(self.future_date))
    
    def test_filter_appointments_by_professional(self):
        #este de filtro de agendamentos por profissional
        self.client.force_authenticate(user=self.normal_user)
        
        # Cria outro profissional e agendamento
        another_professional = HealthProfessional.objects.create(
            social_name='Dr. João Santos',
            profession='Psiquiatra',
            address='Av. Paulista, 1000',
            contact='(11) 98888-8888'
        )
        Appointments.objects.create(
            date=date.today() + timedelta(days=7),
            health_professional=another_professional
        )
        
        # Filtra por profissional
        url = f"{self.list_url}?health_professional={self.health_professional.id}"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['health_professional'], self.health_professional.id)
    
    def test_get_nonexistent_appointment(self):
        self.client.force_authenticate(user=self.normal_user)
        
        nonexistent_url = reverse('appointments-detail-view', kwargs={'pk': 9999})
        response = self.client.get(nonexistent_url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    #TESTS UPDATE
    
    def test_update_appointment_success(self):
        self.client.force_authenticate(user=self.normal_user)
        
        new_date = date.today() + timedelta(days=15)
        data = {
            "date": str(new_date),
            "health_professional": self.health_professional.id
        }
        
        response = self.client.put(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['date'], str(new_date))
    
    def test_partial_update_appointment_success(self):
        self.client.force_authenticate(user=self.normal_user)
        
        new_date = date.today() + timedelta(days=20)
        data = {"date": str(new_date)}
        
        response = self.client.patch(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['date'], str(new_date))
    
    def test_update_appointment_with_past_date(self):
        self.client.force_authenticate(user=self.normal_user)
        
        past_date = date.today() - timedelta(days=3)
        data = {
            "date": str(past_date),
            "health_professional": self.health_professional.id
        }
        
        response = self.client.put(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_update_nonexistent_appointment(self):
        #Teste de atualização de agendamento inexistente
        self.client.force_authenticate(user=self.normal_user)
        
        nonexistent_url = reverse('appointments-detail-view', kwargs={'pk': 9999})
        data = {
            "date": str(date.today() + timedelta(days=10)),
            "health_professional": self.health_professional.id
        }
        
        response = self.client.put(nonexistent_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    #TESTS DELETE 
    
    def test_delete_appointment_success(self):
        #Teste de exclusão de agendamento com sucesso
        self.client.force_authenticate(user=self.normal_user)
        
        response = self.client.delete(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Appointments.objects.count(), 0)
    
    def test_delete_nonexistent_appointment(self):
        #Teste de exclusão de agendamento inexistente
        self.client.force_authenticate(user=self.normal_user)
        
        nonexistent_url = reverse('appointments-detail-view', kwargs={'pk': 9999})
        response = self.client.delete(nonexistent_url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # TESTS without AUTH
    
    def test_unauthorized_create_appointment(self):
        data = {
            "date": str(date.today() + timedelta(days=10)),
            "health_professional": self.health_professional.id
        }
        
        response = self.client.post(self.list_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_unauthorized_list_appointments(self):
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_unauthorized_get_appointment(self):
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_unauthorized_update_appointment(self):
        data = {
            "date": str(date.today() + timedelta(days=10)),
            "health_professional": self.health_professional.id
        }
        
        response = self.client.put(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_unauthorized_delete_appointment(self):
        response = self.client.delete(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
