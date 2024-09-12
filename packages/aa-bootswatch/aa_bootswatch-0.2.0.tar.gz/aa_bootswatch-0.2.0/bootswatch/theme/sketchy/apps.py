from django.apps import AppConfig


class BootstrapThemeConfig(AppConfig):
    name = "bootswatch.theme.sketchy"
    label = "sketchy"
    version = "5.3.3"
    verbose_name = f"Sketchy v{version}"

    def ready(self):
        pass
