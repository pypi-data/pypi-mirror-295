from django.apps import AppConfig


class BootstrapThemeConfig(AppConfig):
    name = "bootswatch.theme.lumen"
    label = "lumen"
    version = "5.3.3"
    verbose_name = f"Lumen v{version}"

    def ready(self):
        pass
