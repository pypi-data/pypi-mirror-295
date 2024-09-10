from pathlib import Path


def merge_settings(*dicts):
    result = {}

    for d in dicts:
        for k, v in d.items():
            if isinstance(v, dict):
                result[k] = merge_settings(result.get(k, {}), v)
            else:
                result[k] = v

    return result


def get_djing_settings(django_settings, inertia_settings):
    BASE_DIR = getattr(django_settings, "BASE_DIR")

    STATIC_ROOT = getattr(django_settings, "STATIC_ROOT", None) or "static"

    DEBUG = getattr(django_settings, "DEBUG", True)

    return {
        "TEMPLATE_DIR_PATH": Path(BASE_DIR) / "djing_resources" / "src",
        "INERTIA": {
            "LAYOUT": "index.html",
            "SSR_URL": inertia_settings.INERTIA_SSR_URL,
            "SSR_ENABLED": inertia_settings.INERTIA_SSR_ENABLED,
            "JSON_ENCODER": inertia_settings.INERTIA_JSON_ENCODER,
        },
        "DJANGO_VITE": {
            "DEV_MODE": DEBUG,
            "SERVER_PROTOCOL": "http",
            "DEV_SERVER_HOST": "localhost",
            "DEV_SERVER_PORT": 5173,
            "WS_CLIENT_URL": "@vite/client",
            "ASSETS_PATH": Path(STATIC_ROOT) / "dist",
            "STATIC_URL_PREFIX": "",
            "LEGACY_POLYFILLS_MOTIF": "legacy-polyfills",
        },
        "STATIC_ROOT": Path(STATIC_ROOT),
        "CSRF_HEADER_NAME": "HTTP_X_XSRF_TOKEN",
        "CSRF_COOKIE_NAME": "XSRF-TOKEN",
    }


def get_settings(django_settings, merged_settings):
    def key_exist(key) -> bool:
        return (
            hasattr(django_settings, key) and getattr(django_settings, key) is not None
        )

    settings = {}

    for key, value in merged_settings.items():
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                sub_key = f"{key}_{sub_key}"
                if not key_exist(sub_key):
                    settings[sub_key] = sub_value
        else:
            if not key_exist(key):
                settings[key] = value

    return settings
