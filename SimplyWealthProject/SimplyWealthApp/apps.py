from django.apps import AppConfig


class SimplywealthappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "SimplyWealthApp"

    def ready(self):
        import SimplyWealthApp.signals
