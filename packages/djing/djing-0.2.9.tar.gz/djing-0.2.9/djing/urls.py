from django.urls import path, re_path
from djing.web import web
from djing.api import api
from djing.views import catch_all_view


def get_url_patterns(prefix: str):
    return [
        path(f"{prefix}/", web.urls),
        path(f"{prefix}/api/", api.urls),
        re_path(rf"^{prefix}/.*$", catch_all_view),
    ]
