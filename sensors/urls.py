from django.urls import path
from . import views

urlpatterns = [
    path('config/<int:sensor_id>/', views.sensors_conf, name='config'),
]
