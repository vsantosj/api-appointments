from django.contrib import admin
from .models import Appointments


@admin.register(Appointments)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'health_professional')
