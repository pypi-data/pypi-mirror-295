from django.apps import AppConfig


class BootstrapThemeConfig(AppConfig):
    name = "bootswatch.theme.cerulean"
    label = "cerulean"
    version = "5.3.3"
    verbose_name = f"Cerulean v{version}"

    def ready(self):
        pass
