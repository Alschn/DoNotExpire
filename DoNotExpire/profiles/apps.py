from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    name = 'DoNotExpire.profiles'

    def ready(self):
        from . import signals
