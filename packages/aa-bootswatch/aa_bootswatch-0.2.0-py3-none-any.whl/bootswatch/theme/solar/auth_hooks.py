from allianceauth import hooks
from allianceauth.theme.hooks import ThemeHook


class SolarThemeHook(ThemeHook):
    """
    Bootswatch Solar Theme
    https://bootswatch.com/solar/
    """

    def __init__(self) -> None:
        ThemeHook.__init__(
            self=self,
            name="Solar",
            description="A spin on Solarized",
            html_tags={"data-theme": "solar"},
            css=[
                {
                    "url": "https://cdnjs.cloudflare.com/ajax/libs/bootswatch/5.3.3/solar/bootstrap.min.css",
                    "integrity": "sha512-0BjJSwKzc+sx3vM/B9nEU98M/hCLM2bcIWrzGe9fqJZFVicDjxu2vrHd0/7ildD+23p5JsQNo8IEL+sOb+A1iw==",
                }
            ],
            js=[
                {
                    "url": "https://cdnjs.cloudflare.com/ajax/libs/popper.js/2.11.8/umd/popper.min.js",
                    "integrity": "sha512-TPh2Oxlg1zp+kz3nFA0C5vVC6leG/6mm1z9+mA81MI5eaUVqasPLO8Cuk4gMF4gUfP5etR73rgU/8PNMsSesoQ==",
                },
                {
                    "url": "https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.3/js/bootstrap.min.js",
                    "integrity": "sha512-ykZ1QQr0Jy/4ZkvKuqWn4iF3lqPZyij9iRv6sGqLRdTPkY69YX6+7wvVGmsdBbiIfN/8OdsI7HABjvEok6ZopQ==",
                },
            ],
            header_padding="3.5em",
        )


@hooks.register("theme_hook")
def register_solar_hook() -> SolarThemeHook:
    return SolarThemeHook()
