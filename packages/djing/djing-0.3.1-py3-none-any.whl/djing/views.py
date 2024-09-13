from django.http import HttpRequest
from inertia import render


def catch_all_view(request: HttpRequest):
    return render(request, "404")
