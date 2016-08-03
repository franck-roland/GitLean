from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from ..config import AUTH_COOKIE
from ..cache import CacheFactory


class GitlabSessionAuthenticationMiddleware(object):

    # Check if client IP is allowed
    def process_view(self, request, callback, callback_args, callback_kwargs):
        if getattr(callback, 'gitlab_auth_exempt', False):
            return None
        if not request.COOKIES.get(AUTH_COOKIE):
            raise PermissionDenied
        private_token = request.COOKIES.get(AUTH_COOKIE)
        setattr(request, 'gitlab_private_token', private_token)

    # def urlredirect(self, request):
    #     path = self.request.build_absolute_uri()
    #     if "something" in path:
    #         URL = "http://www.someurl.com"
    #     else:
    #         URL = "http://www.otherurl.com"
    #     return HttpResponseRedirect(URL)