from django.apps import AppConfig


class BootstrapThemeConfig(AppConfig):
    name = "bootswatch.theme.cyborg"
    label = "cyborg"
    version = "5.3.3"
    verbose_name = f"Cyborg v{version}"

    def ready(self):
        pass
