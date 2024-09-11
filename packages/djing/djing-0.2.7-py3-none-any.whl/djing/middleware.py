from django.http import HttpRequest
from django.conf import settings
from django.contrib.messages import get_messages
from django.template.response import TemplateResponse
from djing.core.application import Application
from inertia import share, render


class DjingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        try:
            application: Application = settings.__getattr__("application")

            if not application.initialized:
                raise ApplicationNotInitializedError()

            share(
                request,
                flash=self.get_flash_messages(request),
                user_id=lambda: request.user.id if request.user else None,
            )

            response = self.get_response(request)

            return response

        except ApplicationNotInitializedError as exception:
            return self.handle_exception(exception, request)

    def get_flash_messages(self, request: HttpRequest):
        flash_messages = {}

        for message in get_messages(request):
            flash_messages = {
                "message": message.message,
                "level": message.level,
                "tags": message.tags,
                "extra_tags": message.extra_tags,
                "level_tag": message.level_tag,
            }

        return flash_messages

    def handle_exception(self, exception: Exception, request: HttpRequest):
        context = {
            "error_message": str(exception),
            "instructions": "Please run the command `python manage.py init` to initialize it.",
        }

        return render(request, "Errors/NotInitialized", {"context": context})


class ApplicationNotInitializedError(Exception):
    def __init__(self):
        super().__init__("Djing application is not initialized.")
