from django.urls import path, re_path

from djing.views import catch_all_view, index, login, process_login

urlpatterns = [
    path("", index, name="index"),
    path("login", login, name="login"),
    path("login", process_login, name="process_login"),
    re_path(r"^.*$", catch_all_view),
]
