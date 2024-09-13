from typing import Any, Self
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect as django_redirect


class Transporter:
    def __init__(self, request: HttpRequest) -> None:
        self.request = request
        self.key = {}
        self.value = {}

    def set(self, key: str, value: Any) -> Self:
        self.key = f"__transport__{key}"
        self.value = value
        return self

    def redirect(self, route: str) -> HttpResponse:
        response: HttpResponse = django_redirect(route)
        response.set_cookie(self.key, self.value)
        return response


def transporter(route):
    return Transporter(route)
