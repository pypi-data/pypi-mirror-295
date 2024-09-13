from functools import wraps
from django.conf import settings
from django.http import HttpRequest
from djing.core.application import Application
from inertia import render


def ensure_initialized(func=None, *, name="guest"):
    def wrapper(f):
        @wraps(f)
        def inner(*args, **kwargs):
            request: HttpRequest = args[0]

            application: Application = settings.__getattr__("application")

            if not application.initialized:
                context = {
                    "error_message": "Djing application is not initialized.",
                    "instructions": "Please run the below command to continue.",
                }

                return render(
                    request,
                    "Errors/ApplicationNotInitialized",
                    {"context": context},
                )

            return f(*args, **kwargs)

        return inner

    if func and callable(func):
        return wrapper(func)
    else:
        return wrapper
