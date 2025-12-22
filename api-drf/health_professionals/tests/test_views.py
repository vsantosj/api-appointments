from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from health_professionals.models import HealthProfessional
from rest_framework_simplejwt.tokens import RefreshToken


class HealthProfessionalCRUDTest(APITestCase):
 
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        
        self.list_create_url = '/api/v1/professionals/'  # AJUSTE A URL
    
    def get_detail_url(self, pk):
        return f'/api/v1/professionals/{pk}/'
    
    def test_create_professional_success(self):
        data = {
            'social_name': 'Dra. Ana Silva',
            'profession': 'Psicóloga',
            'address': 'Rua das Flores, 123',
            'contact': '11999999999'
        }
        response = self.client.post(self.list_create_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(HealthProfessional.objects.count(), 1)
        self.assertEqual(response.data['social_name'], 'Dra. Ana Silva')
    
    def test_create_professional_missing_fields(self):
        """Testa criar profissional sem campos obrigatórios"""
        # Sem nome social
        response = self.client.post(
            self.list_create_url,
            {
                'profession': 'Psicóloga',
                'address': 'Rua das Flores, 123',
                'contact': '11999999999'
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('social_name', response.data)
        
        response = self.client.post(
            self.list_create_url,
            {
                'social_name': 'Dra. Ana Silva',
                'address': 'Rua das Flores, 123',
                'contact': '11999999999'
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('profession', response.data)
    
    def test_create_professional_without_authentication(self):
        self.client.credentials()  # Remove token
        
        data = {
            'social_name': 'Dra. Ana Silva',
            'profession': 'Psicóloga',
            'address': 'Rua das Flores, 123',
            'contact': '11999999999'
        }
        response = self.client.post(self.list_create_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    # ========== READ ==========
    
    def test_list_professionals(self):

        HealthProfessional.objects.create(
            social_name='Dra. Maria',
            profession='Psicóloga',
            address='Rua A, 123',
            contact='11111111111'
        )
        HealthProfessional.objects.create(
            social_name='Dr. João',
            profession='Dentista',
            address='Rua B, 456',
            contact='11222222222'
        )
        HealthProfessional.objects.create(
            social_name='Dra. Carla',
            profession='Nutricionista',
            address='Rua C, 789',
            contact='11333333333'
        )
        
        response = self.client.get(self.list_create_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
    
    def test_list_professionals_empty(self):
        response = self.client.get(self.list_create_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
    
    def test_retrieve_professional(self):
        professional = HealthProfessional.objects.create(
            social_name='Dra. Maria',
            profession='Psicóloga',
            address='Rua A, 123',
            contact='11111111111'
        )
        
        response = self.client.get(self.get_detail_url(professional.id))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], professional.id)
        self.assertEqual(response.data['social_name'], 'Dra. Maria')
    
    def test_retrieve_professional_not_found(self):
        response = self.client.get(self.get_detail_url(99999))
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_professional_put(self):
        """Testa atualizar profissional completamente (PUT)"""
        professional = HealthProfessional.objects.create(
            social_name='Dra. Maria',
            profession='Psicóloga',
            address='Rua A, 123',
            contact='11111111111'
        )
        
        data = {
            'social_name': 'Dra. Maria Santos',
            'profession': 'Psicóloga Clínica',
            'address': 'Rua B, 456',
            'contact': '11999999999'
        }
        response = self.client.put(
            self.get_detail_url(professional.id),
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        professional.refresh_from_db()
        self.assertEqual(professional.social_name, 'Dra. Maria Santos')
        self.assertEqual(professional.address, 'Rua B, 456')
    
    def test_update_professional_patch(self):
        professional = HealthProfessional.objects.create(
            social_name='Dra. Maria',
            profession='Psicóloga',
            address='Rua A, 123',
            contact='11111111111'
        )
        
        response = self.client.patch(
            self.get_detail_url(professional.id),
            {'contact': '11999999999'},
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        professional.refresh_from_db()
        self.assertEqual(professional.contact, '11999999999')
        self.assertEqual(professional.social_name, 'Dra. Maria')  # Outros campos não mudaram
    
    def test_update_professional_not_found(self):
        response = self.client.patch(
            self.get_detail_url(99999),
            {'contact': '11999999999'},
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    
    def test_delete_professional(self):
        professional = HealthProfessional.objects.create(
            social_name='Dra. Maria',
            profession='Psicóloga',
            address='Rua A, 123',
            contact='11111111111'
        )
        
        self.assertEqual(HealthProfessional.objects.count(), 1)
        
        response = self.client.delete(self.get_detail_url(professional.id))
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(HealthProfessional.objects.count(), 0)
    
    def test_delete_professional_not_found(self):
        response = self.client.delete(self.get_detail_url(99999))
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
