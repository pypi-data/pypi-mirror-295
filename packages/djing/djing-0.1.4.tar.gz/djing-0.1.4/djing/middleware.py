from django.contrib.messages import get_messages
from django.http import HttpRequest
from inertia import share


class DjingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        flash_messages = self.get_flash_messages(request)

        share(
            request,
            flash=flash_messages,
            user=lambda: request.user,
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
