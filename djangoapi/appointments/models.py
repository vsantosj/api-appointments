from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
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

    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'
        ordering = ['date']

        # Garante no banco que não há agendamentos duplicados
        unique_together = ['date', 'health_professional']

    def __str__(self):
        return f"Agendamento {self.health_professional} - {self.date}"

    def clean(self):
        if self.date and self.date < timezone.now().date():
            raise ValidationError({
                'date': 'A data não pode ser anterior à data atual.'
            })
