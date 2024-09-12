from django.apps import AppConfig


class BootstrapThemeConfig(AppConfig):
    name = "bootswatch.theme.yeti"
    label = "yeti"
    version = "5.3.3"
    verbose_name = f"Yeti v{version}"

    def ready(self):
        pass
