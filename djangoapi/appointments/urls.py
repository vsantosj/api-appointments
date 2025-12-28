from django.urls import path
from . import views

urlpatterns = [

    path('appointments/', views.AppointmentsCreateView.as_view(), name= 'appointments-create-list'),
    path('appointments/<int:pk>/', views.AppointmentsRetrieveUpdateDestroyAPIView.as_view(), name='appointments-detail-view'),

]
