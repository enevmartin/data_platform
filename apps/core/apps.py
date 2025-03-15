# apps/core/apps.py
from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'
    verbose_name = 'Data Platform Core'

    def ready(self):
        # Import and run admin customization
        from apps.core.admin_config import customize_admin_site
        customize_admin_site()

        # Import signals or perform other initialization if needed
        # import apps.core.signals