from django.apps import AppConfig


class BootstrapThemeConfig(AppConfig):
    name = "bootswatch.theme.journal"
    label = "journal"
    version = "5.3.3"
    verbose_name = f"Journal v{version}"

    def ready(self):
        pass
