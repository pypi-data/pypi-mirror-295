from django.apps import AppConfig


class BootstrapThemeConfig(AppConfig):
    name = "bootswatch.theme.litera"
    label = "litera"
    version = "5.3.3"
    verbose_name = f"Litera v{version}"

    def ready(self):
        pass
