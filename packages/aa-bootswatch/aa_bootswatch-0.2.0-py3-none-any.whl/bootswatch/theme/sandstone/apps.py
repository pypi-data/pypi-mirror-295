from django.apps import AppConfig


class BootstrapThemeConfig(AppConfig):
    name = "bootswatch.theme.sandstone"
    label = "sandstone"
    version = "5.3.3"
    verbose_name = f"Sandstone v{version}"

    def ready(self):
        pass
