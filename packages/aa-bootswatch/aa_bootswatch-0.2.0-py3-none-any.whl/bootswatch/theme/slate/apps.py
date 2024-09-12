from django.apps import AppConfig


class BootstrapThemeConfig(AppConfig):
    name = "bootswatch.theme.slate"
    label = "slate"
    version = "5.3.3"
    verbose_name = f"Slate v{version}"

    def ready(self):
        pass
