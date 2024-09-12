from django.apps import AppConfig


class BootstrapThemeConfig(AppConfig):
    name = "bootswatch.theme.lux"
    label = "lux"
    version = "5.3.3"
    verbose_name = f"Lux v{version}"

    def ready(self):
        pass
