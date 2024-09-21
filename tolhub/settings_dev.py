from .settings import *

DEBUG = True
INSTALLED_APPS = INSTALLED_APPS + [
    "django_seed",
]

THUMBNAILS = {
    "METADATA": {
        "BACKEND": "thumbnails.backends.metadata.DatabaseBackend",
    },
    "STORAGE": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "SIZES": {
        "small": {
            "PROCESSORS": [
                {"PATH": "thumbnails.processors.resize", "width": 10, "height": 10},
                {"PATH": "thumbnails.processors.crop", "width": 80, "height": 80},
            ],
            "POST_PROCESSORS": [
                {
                    "PATH": "thumbnails.post_processors.optimize",
                    "png_command": 'optipng -force -o7 "%(filename)s"',
                    "jpg_command": 'jpegoptim -f --strip-all "%(filename)s"',
                },
            ],
        },
        "large": {
            "PROCESSORS": [
                {"PATH": "thumbnails.processors.resize", "width": 20, "height": 20},
                {"PATH": "thumbnails.processors.flip", "direction": "horizontal"},
            ],
        },
    },
}

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "mediafiles"

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

THUMBNAIL_DEBUG = DEBUG
THUMBNAIL_PREFIX = MEDIA_ROOT / "cache/"


LOGGING = {
    "version": 1,
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
        }
    },
    "loggers": {
        "django.db.backends": {
            "level": "DEBUG",
            "handlers": ["console"],
        }
    },
}
