from django.apps import AppConfig


class BootstrapThemeConfig(AppConfig):
    name = "bootswatch.theme.quartz"
    label = "quartz"
    version = "5.3.3"
    verbose_name = f"Quartz v{version}"

    def ready(self):
        pass
