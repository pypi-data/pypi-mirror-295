from django.apps import AppConfig


class BootstrapThemeConfig(AppConfig):
    name = "bootswatch.theme.united"
    label = "united"
    version = "5.3.3"
    verbose_name = f"United v{version}"

    def ready(self):
        pass
