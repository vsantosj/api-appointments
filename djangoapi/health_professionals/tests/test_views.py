from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from health_professionals.models import HealthProfessional

class HealthProfessionaltestCase(APITestCase):

    def setUp(self):
        self.normal_user = User.objects.create_user(username='userTest', password='userPass')
        self.health_professional = HealthProfessional.objects.create(
            social_name='Dra. Ana Silva',
            profession='Psicóloga',
            address='Rua das Flores, 123',
            contact='(11) 99999-9999'
        )
        self.url = reverse('professionals-detail-view', kwargs={'pk':self.health_professional.pk})
        return super().setUp()


    #Put withou authentication
    def test_unauthorized_update_healthProfessional(self):
        data = {
            "social_name": "update Name",
            "profession": "Psicóloga",
            "address": "Rua das Flores, 123",
            "contact": "(11) 99999-9999"
        }
        response = self.client.put(self.url,data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    #delete without autehnticatin
    def test_unauthorized_delete_healthProfessional(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authorized_update_healthProfessional(self):
        self.client.force_authenticate(user=self.normal_user)
        
        data = {
            "social_name": "update Name",
            "profession": "Psicóloga",
            "address": "Rua das Flores, 123",
            "contact": "(11) 99999-9999"
        }
        response = self.client.put(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authorized_patch_healthProfessional(self):
        self.client.force_authenticate(user=self.normal_user)
        
        data = {"social_name": "update Name"}
        response = self.client.patch(self.url, data, format='json')  # PATCH
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authorized_get_healthProfessional(self):
        self.client.force_authenticate(user=self.normal_user)
        
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['social_name'], 'Dra. Ana Silva')
        self.assertEqual(response.data['profession'], 'Psicóloga')


    def test_authorized_list_healthProfessionals(self):
        self.client.force_authenticate(user=self.normal_user)
        list_url = reverse('professionals-create-list')
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1) 
        self.assertEqual(response.data[0]['social_name'], 'Dra. Ana Silva')


    def test_unauthorized_get_healthProfessional(self):
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_healthProfessional_with_invalid_data(self):
        self.client.force_authenticate(user=self.normal_user)
        
        data = {
            "social_name": "",  # Nome vazio (inválido)
            "profession": "Psicóloga",
            "address": "Rua das Flores, 123",
            "contact": "(11) 99999-9999"
        }
        
        response = self.client.post(
            reverse('professionals-create-list'), 
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('social_name', response.data) 



    def test_create_healthProfessional_with_missing_fields(self):
        self.client.force_authenticate(user=self.normal_user)
        
        data = {
            "social_name": "Dr. João",
        }
        
        response = self.client.post(
            reverse('professionals-create-list'),
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('profession', response.data)
        self.assertIn('address', response.data)
        self.assertIn('contact', response.data)


    def test_get_nonexistent_healthProfessional(self):
        self.client.force_authenticate(user=self.normal_user)
        
        nonexistent_url = reverse('professionals-detail-view', kwargs={'pk': 9999})
        response = self.client.get(nonexistent_url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_nonexistent_healthProfessional(self):
        self.client.force_authenticate(user=self.normal_user)
        
        nonexistent_url = reverse('professionals-detail-view', kwargs={'pk': 9999})
        data = {
            "social_name": "Nome Atualizado",
            "profession": "Psicóloga",
            "address": "Rua Nova, 456",
            "contact": "(11) 88888-8888"
        }
        
        response = self.client.put(nonexistent_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_nonexistent_healthProfessional(self):
        self.client.force_authenticate(user=self.normal_user)
        
        nonexistent_url = reverse('professionals-detail-view', kwargs={'pk': 9999})
        response = self.client.delete(nonexistent_url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_healthProfessional_with_invalid_data(self):
        self.client.force_authenticate(user=self.normal_user)
        
        data = {
            "social_name": "", 
            "profession": "Psicóloga",
            "address": "Rua das Flores, 123",
            "contact": "(11) 99999-9999"
        }
        
        response = self.client.put(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('social_name', response.data)
