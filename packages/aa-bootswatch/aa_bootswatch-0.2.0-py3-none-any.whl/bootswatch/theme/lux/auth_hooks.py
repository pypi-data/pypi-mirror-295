from allianceauth import hooks
from allianceauth.theme.hooks import ThemeHook


class LuxThemeHook(ThemeHook):
    """
    Bootswatch Lux Theme
    https://bootswatch.com/lux/
    """

    def __init__(self) -> None:
        ThemeHook.__init__(
            self=self,
            name="Lux",
            description="A touch of class",
            html_tags={"data-theme": "lux"},
            css=[
                {
                    "url": "https://cdnjs.cloudflare.com/ajax/libs/bootswatch/5.3.3/lux/bootstrap.min.css",
                    "integrity": "sha512-RI2S7J+KOTIVVh6JxrBRNIxJjIioHORVNow+SSz2OMKsDLG5y/YT6iXEK+R0LlKBo/Uwr1O063yT198V6AZh4w==",
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
            header_padding="5.7em",
        )


@hooks.register("theme_hook")
def register_lux_hook() -> LuxThemeHook:
    return LuxThemeHook()
