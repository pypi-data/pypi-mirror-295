from django.apps import AppConfig

from djing.settings import initialize


class DjingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"

    name = "djing"

    def ready(self):
        initialize()

        from djing import urls

        # Import the project's URL patterns
        from django.conf import settings
        from importlib import import_module

        # Get the current urlpatterns from the root URL configuration
        root_urlconf = import_module(settings.ROOT_URLCONF)
        urlpatterns = getattr(root_urlconf, "urlpatterns", [])

        # append django-breeze url patterns
        urlpatterns += urls.urlpatterns

        # Set the modified urlpatterns back to the ROOT_URLCONF setting
        root_urlconf.urlpatterns = urlpatterns
