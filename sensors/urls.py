from django.urls import path
from . import views

urlpatterns = [
    path('config/<int:sensor_id>/', views.sensors_conf, name='config'),
    path('config/schedule/<int:sensor_id>/', views.sensors_conf_schedule, name='config/schedule'),
    path('config/rule/<int:sensor_id>/', views.sensors_conf_rule, name='config/rule')
]
