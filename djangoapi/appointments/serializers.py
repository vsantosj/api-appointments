from rest_framework import serializers
from django.utils import timezone
from appointments.models import Appointments

class AppointmentsModelSerializers(serializers.ModelSerializer):


    class Meta:

        model = Appointments
        fields = '__all__'

    def validate_date(self, value):
            today = timezone.now().date()
            if value < today:
                raise serializers.ValidationError(
                    'A data não pode ser anterior à data atual.'
                )
            return value

    def validate_health_professional(self, value):
            if not value:
                raise serializers.ValidationError(
                    'É obrigatório informar um profissional de saúde.'
                )
            
            return value

    def validate_mult_fields(self, data):
        date = data.get('date')
        professional = data.get('health_professional')

        if date and professional:
            query = Appointments.objects.filter(
                date=date,
                health_professional=professional
            )

            if self.instance:
                query = query.exclude(pk=self.instance.pk)
            
            if query.exists():
                raise serializers.ValidationError(
                    'Este profissional já possui agendamento nesta data.'
                )
        
        return data
