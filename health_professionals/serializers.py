from rest_framework import serializers
from health_professionals.models import HealthProfessional


class HealthProfessionalSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = HealthProfessional
        #campos
        fields = '__all__'
