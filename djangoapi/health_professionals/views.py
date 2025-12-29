from rest_framework import generics
from drf_spectacular.utils import extend_schema
import logging
from health_professionals.models import HealthProfessional
from health_professionals.serializers import HealthProfessionalModelSerializers


logger = logging.getLogger(__name__)


@extend_schema(tags=['Profissionais'])
class HealthProfessionalCreateView(generics.ListCreateAPIView):
    queryset = HealthProfessional.objects.all()
    serializer_class = HealthProfessionalModelSerializers

    @extend_schema(
        summary="Lista ou cria profissionais",
        description="Este endpoint permite listar todos os profissionais ou cadastrar um novo.",
        responses={201: HealthProfessionalModelSerializers}
    )
    def post(self, request, *args, **kwargs):
        logger.info("Criando novo profissional de saúde")
        return super().post(request, *args, **kwargs)

    @extend_schema(summary="Lista todos os profissionais cadastrados")
    def get(self, request, *args, **kwargs):
        logger.info("Listando profissionais de saúde")
        return super().get(request, *args, **kwargs)


@extend_schema(tags=['Profissionais'])
class HealthProfessionalRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HealthProfessional.objects.all()
    serializer_class = HealthProfessionalModelSerializers

    @extend_schema(summary="Busca um profissional específico pelo ID")
    def get(self, request, *args, **kwargs):
        professional_id = kwargs.get('pk')
        logger.info(f"Buscando profissional ID: {professional_id}")
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="Atualiza os dados de um profissional (PUT)")
    def put(self, request, *args, **kwargs):
        professional_id = kwargs.get('pk')
        logger.info(f"Atualizando profissional ID: {professional_id}")
        return super().put(request, *args, **kwargs)

    @extend_schema(summary="Atualiza parcialmente um profissional (PATCH)")
    def patch(self, request, *args, **kwargs):
        professional_id = kwargs.get('pk')
        logger.info(f"Atualizando parcialmente profissional ID: {professional_id}")
        return super().patch(request, *args, **kwargs)

    @extend_schema(summary="Remove um profissional do sistema")
    def delete(self, request, *args, **kwargs):
        professional_id = kwargs.get('pk')
        logger.info(f"Deletando profissional ID: {professional_id}")
        return super().delete(request, *args, **kwargs)
