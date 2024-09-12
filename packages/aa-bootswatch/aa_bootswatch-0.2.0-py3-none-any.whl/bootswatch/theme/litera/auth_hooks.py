from allianceauth import hooks
from allianceauth.theme.hooks import ThemeHook


class LiteraThemeHook(ThemeHook):
    """
    Bootswatch Litera Theme
    https://bootswatch.com/litera/
    """

    def __init__(self) -> None:
        ThemeHook.__init__(
            self=self,
            name="Litera",
            description="The medium is the message",
            html_tags={"data-theme": "litera"},
            css=[
                {
                    "url": "https://cdnjs.cloudflare.com/ajax/libs/bootswatch/5.3.3/litera/bootstrap.min.css",
                    "integrity": "sha512-TUtnNUXMMWp2IALAR9t2z1vuorOUQL4dPWG3J9ANInEj6xu/rz5fzni/faoEGzuqeY1Z1yGD6COYAW72oiDVYA==",
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
            header_padding="3.3em",
        )


@hooks.register("theme_hook")
def register_litera_hook() -> LiteraThemeHook:
    return LiteraThemeHook()
