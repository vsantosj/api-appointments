from django.db import models



class HealthProfessional(models.Model):
    social_name = models.CharField(
        max_length=200, 
        verbose_name='Nome social'
    )
    profession = models.CharField(
        max_length=100, 
        verbose_name='Profissão'
    )
    address = models.TextField(
        verbose_name='Endereço'
    )
    contact = models.CharField(
        max_length=100, 
        verbose_name='Contato'
    )

    class Meta:
        verbose_name = 'Profissional de Saúde'
        verbose_name_plural = 'Profissionais de Saúde'
        ordering = ['social_name']
        constraints = [
            models.UniqueConstraint(
                fields=['social_name', 'profession'],
                name='unique_professional'
            )
        ]

    def __str__(self):
        return f"{self.social_name} - {self.profession}"

    def clean(self):
        if self.social_name:
            self.social_name = ' '.join(self.social_name.split())
        
        if self.profession:
            self.profession = self.profession.strip().title()
        
        if self.contact:
            self.contact = self.contact.strip()
        
        if self.address:
            self.address = self.address.strip()
