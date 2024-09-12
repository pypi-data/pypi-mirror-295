from allianceauth import hooks
from allianceauth.theme.hooks import ThemeHook


class SandstoneThemeHook(ThemeHook):
    """
    Bootswatch Sandstone Theme
    https://bootswatch.com/sandstone/
    """

    def __init__(self) -> None:
        ThemeHook.__init__(
            self=self,
            name="Sandstone",
            description="A touch of warmth",
            html_tags={"data-theme": "sandstone"},
            css=[
                {
                    "url": "https://cdnjs.cloudflare.com/ajax/libs/bootswatch/5.3.3/sandstone/bootstrap.min.css",
                    "integrity": "sha512-0/qBfS6zg4ZK/qvnGwbCpVGDFnfcVnTWhmHgiQNDCcgRLrCBfG4LWAYir/jw/jANoGjEsvQ9ajc9V0j7hxFxag==",
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
def register_sandstone_hook() -> SandstoneThemeHook:
    return SandstoneThemeHook()
