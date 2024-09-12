from allianceauth import hooks
from allianceauth.theme.hooks import ThemeHook


class PulseThemeHook(ThemeHook):
    """
    Bootswatch Pulse Theme
    https://bootswatch.com/pulse/
    """

    def __init__(self) -> None:
        ThemeHook.__init__(
            self=self,
            name="Pulse",
            description="A trace of purple",
            html_tags={"data-theme": "pulse"},
            css=[
                {
                    "url": "https://cdnjs.cloudflare.com/ajax/libs/bootswatch/5.3.3/pulse/bootstrap.min.css",
                    "integrity": "sha512-obkkQCe89/FCOU2KW0b5uQy371PYlf2myYmsVb9EaDeI2t+ZtSec+uSA8HdHFiiNfcLWA8p+nRM3WSHrQKpwuA==",
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
            header_padding="4.9em",
        )


@hooks.register("theme_hook")
def register_pulse_hook() -> PulseThemeHook:
    return PulseThemeHook()
