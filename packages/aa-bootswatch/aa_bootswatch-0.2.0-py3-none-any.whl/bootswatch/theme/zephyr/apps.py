from django.apps import AppConfig


class BootstrapThemeConfig(AppConfig):
    name = "bootswatch.theme.zephyr"
    label = "zephyr"
    version = "5.3.3"
    verbose_name = f"Zephyr v{version}"

    def ready(self):
        pass
