from django.apps import AppConfig


class ManagerConfig(AppConfig):
    name = 'DoNotExpire.manager'

    def ready(self) -> None:
        from . import signals
