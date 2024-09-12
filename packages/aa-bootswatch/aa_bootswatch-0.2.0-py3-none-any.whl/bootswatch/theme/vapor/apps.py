from django.apps import AppConfig


class BootstrapThemeConfig(AppConfig):
    name = "bootswatch.theme.vapor"
    label = "vapor"
    version = "5.3.3"
    verbose_name = f"Vapor v{version}"

    def ready(self):
        pass
