from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def sensors(request):
    return HttpResponse("Hello world!")
