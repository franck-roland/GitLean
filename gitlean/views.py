from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from . import models
from .decorators import gitlab_auth_exempt


@gitlab_auth_exempt
@csrf_exempt
def githook(request):
    models.GitlabHook(request)
    return HttpResponse("")
