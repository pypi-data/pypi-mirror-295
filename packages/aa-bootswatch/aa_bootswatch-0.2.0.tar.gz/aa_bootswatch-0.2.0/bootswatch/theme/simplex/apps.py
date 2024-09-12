from django.apps import AppConfig


class BootstrapThemeConfig(AppConfig):
    name = "bootswatch.theme.simplex"
    label = "simplex"
    version = "5.3.3"
    verbose_name = f"Simplex v{version}"

    def ready(self):
        pass
