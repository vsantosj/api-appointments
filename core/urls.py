from django.contrib import admin
from django.urls import path
from health_professionals.views import HealthProfessionalCreateView, HealthProfessionalRetrieveUpdateDestroyView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    path('admin/', admin.site.urls),

    path('professionals/', HealthProfessionalCreateView.as_view(), name='professionals-create-list'),
    path('professionals/<int:pk>',HealthProfessionalRetrieveUpdateDestroyView.as_view(), name='professionals-detail-view'),


    # Gera o arquivo YAML/JSON da documentação
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    
    # Interface visual do Swagger
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # Interface alternativa Redoc (Opcional)
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
