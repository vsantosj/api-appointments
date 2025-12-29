from rest_framework import generics
from drf_spectacular.utils import extend_schema
import logging
from django_filters.rest_framework import DjangoFilterBackend
from appointments.serializers import AppointmentsModelSerializers
from appointments.models import Appointments


logger = logging.getLogger(__name__)


@extend_schema(tags=['Appointments'])
class AppointmentsCreateView(generics.ListCreateAPIView):
    queryset = Appointments.objects.all()
    serializer_class = AppointmentsModelSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['health_professional']

    @extend_schema(
        summary="Lista ou cria Agendamentos",
        description="Este endpoint permite listar todos os agendametnos ou cadastrar um novo.",
        responses={201: AppointmentsModelSerializers}
    )
    def post(self, request, *args, **kwargs):
        logger.info('Criando novo agendamento')
        try:
            response = super().post(request, *args, **kwargs)
            logger.info(f"Agendamento criado - ID: {response.data.get('id')}")
            return response
        except Exception as e:
            logger.error(f"Erro ao criar agendamento: {str(e)}")
            raise

    @extend_schema(
        summary="Lista agendamentos com filtros opcionais",
        description="Filtre usando os parâmetros 'health_professional' (ID) ou 'data' (YYYY-MM-DD)."
    )
    def get(self, request, *args, **kwargs):
        logger.info(f"Usuário {request.user} listando agendamentos")
        return super().get(request, *args, **kwargs)


@extend_schema(tags=['Appointments'])
class AppointmentsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appointments.objects.all()
    serializer_class = AppointmentsModelSerializers

    @extend_schema(summary="Busca um Agendamento específico pelo ID")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="Atualiza os dados de um agendamento (PUT)")
    def put(self, request, *args, **kwargs):
        appointment_id = kwargs.get('pk')
        logger.info(f"Usuário {request.user} atualizando agendamento ID: {appointment_id}")
        return super().put(request, *args, **kwargs)

    @extend_schema(summary="Atualiza parcialmente um agendamento (PATCH)")
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(summary="Remove um agendamento do sistema")
    def delete(self, request, *args, **kwargs):
        appointment_id = kwargs.get('pk')
        logger.warning(f"Usuário {request.user} deletando agendamento ID: {appointment_id}")
        return super().delete(request, *args, **kwargs)
