from rest_framework import generics
from health_professionals.models import HealthProfessional
from health_professionals.serializers import HealthProfessionalSerializers
from drf_spectacular.utils import extend_schema


@extend_schema(tags=['Profissionais'])
class HealthProfessionalCreateView(generics.ListCreateAPIView):
    queryset = HealthProfessional.objects.all()
    serializer_class = HealthProfessionalSerializers

    @extend_schema(
        summary="Lista ou cria profissionais",
        description="Este endpoint permite listar todos os profissionais ou cadastrar um novo.",
        responses={201: HealthProfessionalSerializers}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    @extend_schema(summary="Lista todos os profissionais cadastrados")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@extend_schema(tags=['Profissionais'])
class HealthProfessionalRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HealthProfessional.objects.all()
    serializer_class = HealthProfessionalSerializers
    
    @extend_schema(summary="Busca um profissional específico pelo ID")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="Atualiza os dados de um profissional (PUT)")
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(summary="Atualiza parcialmente um profissional (PATCH)")
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(summary="Remove um profissional do sistema")
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
