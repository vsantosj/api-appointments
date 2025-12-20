from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from health_professionals.views import HealthProfessionalCreateView, HealthProfessionalRetrieveUpdateDestroyView
from appointments.views import AppointmentsCreateView, AppointmentsRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/professionals/', HealthProfessionalCreateView.as_view(), name='professionals-create-list'),
    path('api/professionals/<int:pk>',HealthProfessionalRetrieveUpdateDestroyView.as_view(), name='professionals-detail-view'),

    path('api/appointments/', AppointmentsCreateView.as_view(), name= 'appointments-create-list'),
    path('api/appointments/<int:pk>', AppointmentsRetrieveUpdateDestroyAPIView.as_view(), name='appointments-detail-view'),


    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
