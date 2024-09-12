from allianceauth import hooks
from allianceauth.theme.hooks import ThemeHook


class SuperheroThemeHook(ThemeHook):
    """
    Bootswatch Superhero Theme
    https://bootswatch.com/superhero/
    """

    def __init__(self) -> None:
        ThemeHook.__init__(
            self=self,
            name="Superhero",
            description="The brave and the blue",
            html_tags={"data-theme": "superhero"},
            css=[
                {
                    "url": "https://cdnjs.cloudflare.com/ajax/libs/bootswatch/5.3.3/superhero/bootstrap.min.css",
                    "integrity": "sha512-yeFVFyLRIY48erNjFZ1uXiERPXN8izq4mBNe4iSgVYT0bq/ZiSsWwTlaSObBDeqR/+7MBw1g23iSpI9ru/qtGQ==",
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
def register_superhero_hook():
    return SuperheroThemeHook()
