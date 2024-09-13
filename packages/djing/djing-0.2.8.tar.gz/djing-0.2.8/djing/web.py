from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse

from djing.decorators.login_required import login_required
from djing.decorators.ensure_initialized import ensure_initialized

from ninja import NinjaAPI
from inertia import render

web = NinjaAPI(urls_namespace="web")


@web.get("/login")
@ensure_initialized
def login(request: HttpRequest):
    return render(request, "Account/Login")


@web.get("/", url_name="home")
@ensure_initialized
def index(request: HttpRequest):
    dashboard_route = reverse("web:dashboard")
    return redirect(dashboard_route)


@web.get("/dashboard", url_name="dashboard")
@ensure_initialized
@login_required
def dashboard(request: HttpRequest):
    packages = ["Django", "Inertia.js", "Vite.js"]

    return render(request, "Index", {"packages": packages})
