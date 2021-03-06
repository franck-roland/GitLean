from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from . import models


@csrf_exempt
def githook(request):
    models.GitlabHook(request)
    return HttpResponse("")
