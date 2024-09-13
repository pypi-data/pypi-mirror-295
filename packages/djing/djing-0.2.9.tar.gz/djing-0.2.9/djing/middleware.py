from django.http import HttpRequest
from django.contrib.messages import get_messages
from inertia import share

from djing.core.application import Application
from django.conf import settings


class DjingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        application: Application = settings.__getattr__("application")

        application.set_base_url(request)

        djing_config = {
            "base_url": application.base_url,
            "auth": application.auth,
        }

        share(
            request,
            errors=lambda: request.session.pop("errors", {}),
            flash=self.get_flash_messages(request),
            user_id=lambda: request.user.id if request.user else None,
            djing_config=djing_config,
        )

        response = self.get_response(request)

        return response

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
