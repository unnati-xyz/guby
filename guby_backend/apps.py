from django.apps import AppConfig


class GubyBackendConfig(AppConfig):
    name = 'guby_backend'

    def ready(self):
        import guby_backend.signals