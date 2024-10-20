from django.apps import AppConfig


class PanelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'panel'

    def ready(self) -> None:
        from . import signals
