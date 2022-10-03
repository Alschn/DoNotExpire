from django.apps import AppConfig


class ManagerConfig(AppConfig):
    name = 'manager'

    def ready(self) -> None:
        from . import signals
