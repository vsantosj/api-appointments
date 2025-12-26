from rest_framework import serializers
import re
from health_professionals.models import HealthProfessional


class HealthProfessionalModelSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = HealthProfessional
        fields = '__all__'

    def validate_social_name(self, value):
        value = ' '.join(value.split())

        if len(value.strip()) < 3:
            raise serializers.ValidationError(
                'O nome social deve ter pelo menos 3 caracteres.'
            )       
        if len(value) > 200:
            raise serializers.ValidationError(
                'O nome social não pode exceder 200 caracteres.'
            )       
        if value.strip().isdigit():
            raise serializers.ValidationError(
                'O nome social não pode conter apenas números.'
            )       
        return value.strip()

    def validate_profession(self, value):
        value = ' '.join(value.split())    
        if not value.strip():
            raise serializers.ValidationError(
                'A profissão é obrigatória.'
            )    
        if len(value.strip()) < 3:
            raise serializers.ValidationError(
                'A profissão deve ter pelo menos 3 caracteres.'
            )
        value = value.strip().title()
        return value
    
    def validate_address(self, value):
        value = re.sub(r'\s+', ' ', value)
        value = re.sub(r'\n\s*\n', '\n', value)
        
        if len(value.strip()) < 10:
            raise serializers.ValidationError(
                'O endereço deve ter pelo menos 10 caracteres.'
            )

        if len(value) > 500:
            raise serializers.ValidationError(
                'O endereço não pode exceder 500 caracteres.'
            )
        
        return value.strip()
    
    def validate_contact(self, value): 
        value = ' '.join(value.split()).strip()
        if not value:
            raise serializers.ValidationError(
                'O contato é obrigatório.'
            )    
        if len(value) < 11:
            raise serializers.ValidationError(
                'O contato deve ter pelo menos 8 caracteres.'
            )

        only_digits = re.sub(r'\D', '', value)
        
        if only_digits and len(only_digits) < 10:
            raise serializers.ValidationError(
                'Telefone inválido. Deve conter DDD + número.'
            )       
        return value

    def validate_mult_fields(self, data):
        social_name = data.get('social_name', '')
        profession = data.get('profession', '')

        if social_name and profession:
            query = HealthProfessional.objects.filter(
                social_name__iexact=social_name.strip(),
                profession__iexact=profession.strip()
            )

            if self.instance:
                query = query.exclude(pk=self.instance.pk)
            
            if query.exists():
                raise serializers.ValidationError(
                    'Já existe um profissional cadastrado com este nome e profissão.'
                )     
        return data
