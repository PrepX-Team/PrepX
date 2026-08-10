from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from functools import wraps


def role_required(allowed_roles):
    """
    Usage: @role_required(['admin', 'teacher'])
    Must be stacked UNDER @login_required (or this handles it too).
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            if request.user.role not in allowed_roles:
                return HttpResponseForbidden(
                    "You are not authorized to access this page."
                )
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator