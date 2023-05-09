from django.urls import path
from . import views

urlpatterns = [
    path('sensors/', views.sensors, name='sensors'),
]
