from django.apps import AppConfig


class BootstrapThemeConfig(AppConfig):
    name = "bootswatch.theme.solar"
    label = "solar"
    version = "5.3.3"
    verbose_name = f"Solar v{version}"

    def ready(self):
        pass
