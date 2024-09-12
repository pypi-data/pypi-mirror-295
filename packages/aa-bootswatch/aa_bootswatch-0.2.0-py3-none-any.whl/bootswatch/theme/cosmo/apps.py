from django.apps import AppConfig


class BootstrapThemeConfig(AppConfig):
    name = "bootswatch.theme.cosmo"
    label = "cosmo"
    version = "5.3.3"
    verbose_name = f"Cosmo v{version}"

    def ready(self):
        pass
