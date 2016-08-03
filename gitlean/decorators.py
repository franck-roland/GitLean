from functools import wraps
from django.utils.decorators import available_attrs


def gitlab_auth_exempt(view_func):
    """
    Marks a view function as being exempt from the CSRF view protection.
    """
    # We could just do view_func.gitlab_auth_exempt = True, but decorators
    # are nicer if they don't have side-effects, so we return a new
    # function.
    def wrapped_view(*args, **kwargs):
        return view_func(*args, **kwargs)
    wrapped_view.gitlab_auth_exempt = True
    return wraps(view_func, assigned=available_attrs(view_func))(wrapped_view)
