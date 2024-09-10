import django

VERSION = (1, 7, 2)

if django.VERSION < (3, 2):
    default_app_config = "django_q.apps.DjangoQConfig"

__all__ = ["conf", "cluster", "models", "tasks"]
