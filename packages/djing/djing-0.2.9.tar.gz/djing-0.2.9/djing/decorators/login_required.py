from functools import wraps
from django.conf import settings
from django.http import HttpRequest
from django.shortcuts import redirect

from djing.core.application import Application


def login_required(func=None):
    def wrapper(f):
        @wraps(f)
        def inner(*args, **kwargs):
            request: HttpRequest = args[0]

            if not request.user.is_authenticated:
                application: Application = settings.__getattr__("application")

                return redirect(f"{application.base_url}/login")

            return f(*args, **kwargs)

        return inner

    if func and callable(func):
        return wrapper(func)
    else:
        return wrapper
