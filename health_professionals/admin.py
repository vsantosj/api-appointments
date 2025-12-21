from django.contrib import admin
from .models import HealthProfessional

@admin.register(HealthProfessional)
class HealthProfessionalAdmin(admin.ModelAdmin):
    list_display = ('id', 'social_name', 'profession', 'address', 'contact')
