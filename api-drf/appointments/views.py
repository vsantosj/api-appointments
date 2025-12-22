from rest_framework import generics
from drf_spectacular.utils import extend_schema
from django_filters.rest_framework import DjangoFilterBackend
from appointments.serializers import AppointmentsModelSerializers
from appointments.models import Appointments


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
        return super().post(request, *args, **kwargs)

    @extend_schema(
        summary="Lista agendamentos com filtros opcionais",
        description="Filtre usando os parâmetros 'health_professional' (ID) ou 'data' (YYYY-MM-DD)."
    )
    def get(self, request, *args, **kwargs):
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
        return super().put(request, *args, **kwargs)

    @extend_schema(summary="Atualiza parcialmente um agendamento (PATCH)")
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(summary="Remove um agendamento do sistema")
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
