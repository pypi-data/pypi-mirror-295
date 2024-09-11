from django.apps import AppConfig

from djing.settings import initialize


class DjingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"

    name = "djing"

    def ready(self):
        initialize()
