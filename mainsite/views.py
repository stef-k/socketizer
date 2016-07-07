import requests

from django.http import JsonResponse
from django.shortcuts import render
from .models import Settings


# Create your views here.
def index(request):
    return render(request, 'index.html')


def pool_info(request):

    settings = Settings.objects.all()[0]

    url = 'http://localhost:8080/service/api/v1/pool-info'
    data = {'serviceKey': settings.service_key}

    try:
        response = requests.post(url, json=data)

        return JsonResponse(response.json())
    except Exception:
        return JsonResponse({"DomainCount": 0, "ClientSub": 0})
