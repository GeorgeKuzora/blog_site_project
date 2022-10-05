from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users_app"
    verbose_name = _('users')
