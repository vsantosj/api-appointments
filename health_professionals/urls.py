from django.urls import path
from . import views


urlpatterns =[
    path('professionals/', views.HealthProfessionalCreateView.as_view(), name='professionals-create-list'),
    path('professionals/<int:pk>/',views.HealthProfessionalRetrieveUpdateDestroyView.as_view(), name='professionals-detail-view'),
]
