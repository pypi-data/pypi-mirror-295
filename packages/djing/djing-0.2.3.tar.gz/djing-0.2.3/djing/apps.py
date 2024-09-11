from django.apps import AppConfig
from djing.core.inertia_app import InertiaApp
from djing.core.application import Application


class DjingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"

    name = "djing"

    def ready(self):
        inertia_app = InertiaApp()

        application = Application(inertia_app)

        application.run()
