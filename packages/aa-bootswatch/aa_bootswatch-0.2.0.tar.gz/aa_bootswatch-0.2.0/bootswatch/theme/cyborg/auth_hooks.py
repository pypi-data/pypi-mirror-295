from allianceauth import hooks
from allianceauth.theme.hooks import ThemeHook


class CyborgThemeHook(ThemeHook):
    """
    Bootswatch cyborg Theme
    https://bootswatch.com/cyborg/
    """

    def __init__(self) -> None:
        ThemeHook.__init__(
            self=self,
            name="Cyborg",
            description="Jet black and electric blue",
            html_tags={"data-theme": "cyborg"},
            css=[
                {
                    "url": "https://cdnjs.cloudflare.com/ajax/libs/bootswatch/5.3.3/cyborg/bootstrap.min.css",
                    "integrity": "sha512-M+Wrv9LTvQe81gFD2ZE3xxPTN5V2n1iLCXsldIxXvfs6tP+6VihBCwCMBkkjkQUZVmEHBsowb9Vqsq1et1teEg==",
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
            header_padding="3.6em",
        )


@hooks.register("theme_hook")
def register_cyborg_hook() -> CyborgThemeHook:
    return CyborgThemeHook()
