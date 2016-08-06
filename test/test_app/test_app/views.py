from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from gitlean import controllers
from gitlean.decorators import gitlab_auth_exempt
from gitlean import config


def test(request):
    project = [project for project in controllers.ProjectController().findAll() if project.name == 'test-git-hook'][0]
    issues = controllers.IssueController(project).findAll()
    return render(request, 'test_app/index.html', {'project': project, 'issues': issues})


@gitlab_auth_exempt
def authenticate(request):
    if request.method == "POST":
        private_token = controllers.Login.get_private_token(request.POST['login'], request.POST['password'])
        if private_token:
            response = render(request, 'test_app/login.html')
            response.set_cookie(config.AUTH_COOKIE, private_token)
            return response
    project = [project for project in controllers.ProjectController().findAll() if project.name == 'test-git-hook'][0]
    issues = controllers.IssueController(project).findAll()
    return render(request, 'test_app/login.html', {'project': project, 'issues': issues})
