from allianceauth import hooks
from allianceauth.theme.hooks import ThemeHook


class LumenThemeHook(ThemeHook):
    """
    Bootswatch Lumen Theme
    https://bootswatch.com/lumen/
    """

    def __init__(self) -> None:
        ThemeHook.__init__(
            self=self,
            name="Lumen",
            description="Light and shadow",
            html_tags={"data-theme": "lumen"},
            css=[
                {
                    "url": "https://cdnjs.cloudflare.com/ajax/libs/bootswatch/5.3.3/lumen/bootstrap.min.css",
                    "integrity": "sha512-N6Wwrw2+w72hDf55YI/j+y3JUXpO7qTuo+kilvcpFJqEabBFA3nurVZineUcg4+op0dJLrzQXcNNif9Gf/ECPA==",
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
            header_padding="3.7em",
        )


@hooks.register("theme_hook")
def register_lumen_hook() -> LumenThemeHook:
    return LumenThemeHook()
