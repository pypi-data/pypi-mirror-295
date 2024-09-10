import inertia

from pathlib import Path
from django.conf import settings as django_settings
from inertia.settings import settings as inertia_settings
from djing.libs.helpers import (
    get_djing_settings,
    get_settings,
    merge_settings,
)


def initialize():
    MIDDLEWARES = [
        "inertia.middleware.InertiaMiddleware",
        "djing.middleware.DjingMiddleware",
    ]

    djing_settings = get_djing_settings(django_settings, inertia_settings)

    user_settings = getattr(django_settings, "DJING", {})

    merged_settings = merge_settings(djing_settings, user_settings)

    settings = get_settings(django_settings, merged_settings)

    for key, value in settings.items():
        setattr(django_settings, key, value)

    TEMPLATE_DIR_PATH = Path(getattr(django_settings, "TEMPLATE_DIR_PATH"))

    DJANGO_VITE_ASSETS_PATH = Path(getattr(django_settings, "DJANGO_VITE_ASSETS_PATH"))

    django_settings.TEMPLATES[0]["DIRS"].extend(
        [TEMPLATE_DIR_PATH, Path(inertia.__file__).resolve().parent / "templates/"]
    )

    django_settings.STATICFILES_DIRS.extend(
        [
            DJANGO_VITE_ASSETS_PATH,
            TEMPLATE_DIR_PATH / "assets",
            TEMPLATE_DIR_PATH / "public",
        ]
    )

    for middleware in MIDDLEWARES:
        django_settings.MIDDLEWARE.append(middleware)
