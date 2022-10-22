"""
To render html web pages
"""
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template import loader
from sensors.models import Sensor


def indx_view(request):
    """
    Take in a request and return HTML
    """

    sensors = Sensor.objects.all().values()
    template = loader.get_template("index.html")
    context = {
        'sensors': sensors,
    }
    return HttpResponse(template.render(context, request))
