from rest_framework import serializers
from django.utils import timezone
from django.core.exceptions import ValidationError
from appointments.models import Appointments

class AppointmentsModelSerializers(serializers.ModelSerializer):


    class Meta:
        model = Appointments
        fields = '__all__'

    def validate_date(self,value):
        if value < timezone.now().date():
            raise serializers.ValidationError('A data não pode ser inferior à data atual.')
        
        return value
