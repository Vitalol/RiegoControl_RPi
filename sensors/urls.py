from django.urls import path
from . import views

urlpatterns = [
    path('sensor/<int:sensor_id>/', views.sensor_graph, name='sensor_graph'),
    path('config/actuator/<int:actuator_id>/', views.actuator_conf, name='config/actuator'),
    path('config/actuator/rule/<int:actuator_id>/', views.actuator_conf_rule, name='config/actuator/rule'),
    path('config/actuator/schedule/<int:actuator_id>/', views.actuator_conf_schedule, name='config/actuator/schedule'),
    path('config/actuator/manual/<int:actuator_id>/', views.actuator_conf_manual, name='config/actuator/manual'),
]
