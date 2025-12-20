from rest_framework import serializers
from appointments.models import Appointments

class AppointmentsSerializers(serializers.ModelSerializer):

    class Meta:
        model = Appointments
        fields = '__all__'
