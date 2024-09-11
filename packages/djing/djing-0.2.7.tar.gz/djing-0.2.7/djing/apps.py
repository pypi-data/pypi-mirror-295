from django.apps import AppConfig
from django.conf import settings
from djing.core.inertia_app import InertiaApp
from djing.core.application import Application


class DjingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"

    name = "djing"

    def ready(self):
        inertia_app = InertiaApp()

        inertia_app.boot()

        application = Application()

        application.run()

        settings.__setattr__("application", application)
