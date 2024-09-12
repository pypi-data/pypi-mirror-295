from allianceauth import hooks
from allianceauth.theme.hooks import ThemeHook


class JournalThemeHook(ThemeHook):
    """
    Bootswatch Journal Theme
    https://bootswatch.com/journal/
    """

    def __init__(self) -> None:
        ThemeHook.__init__(
            self=self,
            name="Journal",
            description="Crisp like a new sheet of paper",
            html_tags={"data-theme": "journal"},
            css=[
                {
                    "url": "https://cdnjs.cloudflare.com/ajax/libs/bootswatch/5.3.3/journal/bootstrap.min.css",
                    "integrity": "sha512-i0XjXal2VCWv2R9nyqgvp/pPZGTG563h0djHqDDgu/8S9EIsLNpv+9WoqQFu3ngwDyD5I5WvwauQM1gyNXxsRw==",
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
def register_journal_hook() -> JournalThemeHook:
    return JournalThemeHook()
