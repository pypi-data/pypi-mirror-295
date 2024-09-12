from allianceauth import hooks
from allianceauth.theme.hooks import ThemeHook


class ZephyrThemeHook(ThemeHook):
    """
    Bootswatch Zephyr Theme
    https://bootswatch.com/zephyr/
    """

    def __init__(self) -> None:
        ThemeHook.__init__(
            self=self,
            name="Zephyr",
            description="Breezy and beautiful",
            html_tags={"data-theme": "zephyr"},
            css=[
                {
                    "url": "https://cdnjs.cloudflare.com/ajax/libs/bootswatch/5.3.3/zephyr/bootstrap.min.css",
                    "integrity": "sha512-CWXb9sx63+REyEBV/cte+dE1hSsYpJifb57KkqAXjsN3gZQt6phZt7e5RhgZrUbaNfCdtdpcqDZtuTEB+D3q2Q==",
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
            header_padding="4.2em",
        )


@hooks.register("theme_hook")
def register_zephyr_hook() -> ZephyrThemeHook:
    return ZephyrThemeHook()
