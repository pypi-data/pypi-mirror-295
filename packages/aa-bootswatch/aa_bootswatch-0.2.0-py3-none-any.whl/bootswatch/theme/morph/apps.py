from django.apps import AppConfig


class BootstrapThemeConfig(AppConfig):
    name = "bootswatch.theme.morph"
    label = "morph"
    version = "5.3.3"
    verbose_name = f"Morph v{version}"

    def ready(self):
        pass
