from django.apps import AppConfig


class BootstrapThemeConfig(AppConfig):
    name = "bootswatch.theme.spacelab"
    label = "spacelab"
    version = "5.3.3"
    verbose_name = f"Spacelab v{version}"

    def ready(self):
        pass
