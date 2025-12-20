from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from health_professionals.models import HealthProfessional

def validate_date_not_past(value):
    if value < timezone.now().date():
        raise ValidationError('A data não pode ser inferior à data atual.')

class Appointments(models.Model):
    data = models.DateField(
        verbose_name='Data',
        validators=[validate_date_not_past]
    )
    health_professional = models.ForeignKey(
        HealthProfessional, 
        on_delete=models.PROTECT,
        related_name='appointments',
        verbose_name="Profissional"
    )
