from django.apps import AppConfig


class BootstrapThemeConfig(AppConfig):
    name = "bootswatch.theme.pulse"
    label = "pulse"
    version = "5.3.3"
    verbose_name = f"Pulse v{version}"

    def ready(self):
        pass
