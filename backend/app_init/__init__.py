from django.apps import AppConfig


class AppDictConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_init'

    def ready(self):
        import app_init.management.commands
