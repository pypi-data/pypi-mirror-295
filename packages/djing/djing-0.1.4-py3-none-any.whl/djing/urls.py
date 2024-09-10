from django.urls import path
from djing.views import index

urlpatterns = [
    path("", index, name="index"),
]
