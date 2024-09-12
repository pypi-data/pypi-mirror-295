from django.apps import AppConfig


class BootstrapThemeConfig(AppConfig):
    name = "bootswatch.theme.superhero"
    label = "superhero"
    version = "5.3.3"
    verbose_name = f"Superhero v{version}"

    def ready(self):
        pass
