from allianceauth import hooks
from allianceauth.theme.hooks import ThemeHook


class YetiThemeHook(ThemeHook):
    """
    Bootswatch Yeti Theme
    https://bootswatch.com/yeti/
    """

    def __init__(self) -> None:
        ThemeHook.__init__(
            self=self,
            name="Yeti",
            description="A friendly foundation",
            html_tags={"data-theme": "yeti"},
            css=[
                {
                    "url": "https://cdnjs.cloudflare.com/ajax/libs/bootswatch/5.3.3/yeti/bootstrap.min.css",
                    "integrity": "sha512-Iwexq+Vk4qT5CCO6UdOTzOxJUB0eQxAWAfm6ytWws6MMcD6illgOw7QFjWoqqd3bQJS/EZPUR9nOACG7i5WMPQ==",
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
def register_yeti_hook() -> YetiThemeHook:
    return YetiThemeHook()
