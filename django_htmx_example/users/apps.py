from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "django_htmx_example.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import django_htmx_example.users.signals  # noqa F401
        except ImportError:
            pass
