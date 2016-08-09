import requests

from django.http import JsonResponse
from django.shortcuts import render
from .models import Settings, Statistics
import logging

log = logging.getLogger(__name__)


# Create your views here.
def index(request):
    settings = Settings.objects.first()
    stats = Statistics.objects.first()
    return render(request, 'index.html',
                  {'settings': settings,
                   'stats': stats})


def pool_info(request):
    settings = Settings.objects.all()[0]

    url = 'https://service.socketizer.com/service/api/v1/pool-info'
    data = {'serviceKey': settings.service_key}

    try:
        response = requests.post(url, json=data)
        log.debug('pool-info request results: {}'.format(response.json()))
        return JsonResponse(response.json())
    except Exception as e:
        log.debug('could not complete pool-info request {}'.format(e))
        return JsonResponse({"DomainCount": 0, "ClientSub": 0})
