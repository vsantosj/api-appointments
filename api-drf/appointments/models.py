from django.db import models

from health_professionals.models import HealthProfessional



class Appointments(models.Model):
    date = models.DateField(
        verbose_name='Data',
    )
    health_professional = models.ForeignKey(
        HealthProfessional, 
        on_delete=models.PROTECT,
        related_name='appointments',
        verbose_name="Profissional"
    )
