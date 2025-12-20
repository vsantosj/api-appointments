from django.db import models

class HealthProfessional(models.Model):
    social_name = models.CharField(max_length=200, verbose_name='Nome social')
#    profession = models.CharField(max_length=100, verbose_name='Profissão')
#    address = models.TextField(verbose_name='Endereço')
#    contact = models.CharField(max_length=100, verbose_name='Contato')
