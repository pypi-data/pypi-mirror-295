from django.http import HttpRequest
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods

from inertia import render


def login(request: HttpRequest):
    print(request.inertia.props)
    return render(request, "Account/Login")


@require_http_methods(["POST"])
def process_login(request: HttpRequest):
    return "test"


def index(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect("dashboard")
    else:
        return redirect("login")


def dashboard(request: HttpRequest):
    packages = ["Django", "Inertia.js", "Vite.js"]

    return render(request, "Index", {"packages": packages})


def catch_all_view(request: HttpRequest):
    return render(request, "404")
