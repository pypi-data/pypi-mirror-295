from functools import wraps
from typing import Callable, Literal, Optional
from django.conf import settings
from django.http import HttpRequest
from django.shortcuts import redirect
from djing.core.application import Application


def get_application() -> Application:
    """Helper function to get the application object."""
    return settings.__getattr__("application")


def access_required(
    func: Optional[Callable] = None,
    *,
    allowed_user_type: Literal["guest", "authenticated"] = "guest",
):
    """Decorator to enforce login requirements based on user type."""

    def decorator(view_func: Callable):
        @wraps(view_func)
        def wrapper(request: HttpRequest, *args, **kwargs):
            if not isinstance(request, HttpRequest):
                raise TypeError("Expected an instance of HttpRequest")

            application = get_application()

            if (
                allowed_user_type == "authenticated"
                and not request.user.is_authenticated
            ):
                return redirect(f"{application.base_url}/login")

            if allowed_user_type == "guest" and request.user.is_authenticated:
                print("test")
                return redirect(f"{application.base_url}/dashboard")

            return view_func(request, *args, **kwargs)

        return wrapper

    if func:
        return decorator(func)

    return decorator
