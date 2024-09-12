from django.apps import AppConfig


class BootstrapThemeConfig(AppConfig):
    name = "bootswatch.theme.minty"
    label = "minty"
    version = "5.3.3"
    verbose_name = f"Minty v{version}"

    def ready(self):
        pass
