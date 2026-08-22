from functools import wraps  # wraps avoids 'wrapper' in the system logs

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.template.loader import render_to_string # to load a custom HTML template directly into the Python logic


def role_required(*allowed_roles):
    """
    Usage:
        @role_required('admin')
        @role_required('admin', 'teacher')
    """

    def decorator(view_func):

        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            if request.user.role not in allowed_roles:
                html = render_to_string(
                    '403.html',
                    {},
                    request=request
                )
                return HttpResponseForbidden(html)

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator