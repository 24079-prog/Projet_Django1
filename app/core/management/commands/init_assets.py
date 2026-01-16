from django.core.management.base import BaseCommand
from core.models import Asset

ASSETS = [
    # Devises
    {"code": "USD", "label": "US Dollar", "category": "currency",
     "api_source": "frankfurter", "api_symbol": "USD", "base_currency": "USD"},
    {"code": "EUR", "label": "Euro", "category": "currency",
     "api_source": "frankfurter", "api_symbol": "EUR", "base_currency": "EUR"},
    {"code": "CNY", "label": "Yuan", "category": "currency",
     "api_source": "frankfurter", "api_symbol": "CNY", "base_currency": "CNY"},

    # Crypto
    {"code": "BTC", "label": "Bitcoin", "category": "crypto",
     "api_source": "coingecko", "api_symbol": "bitcoin", "base_currency": "USD"},

    # Métaux
    {"code": "GOLD", "label": "Gold", "category": "commodity",
     "api_source": "metalsapi", "api_symbol": "XAU", "base_currency": "USD"},
    {"code": "IRON", "label": "Iron", "category": "commodity",
     "api_source": "metalsapi", "api_symbol": "IRON", "base_currency": "USD"},
    {"code": "COPPER", "label": "Copper", "category": "commodity",
     "api_source": "metalsapi", "api_symbol": "COPPER", "base_currency": "USD"},
]

class Command(BaseCommand):
    help = "Initialise les assets avec leurs sources API"

    def handle(self, *args, **kwargs):
        for a in ASSETS:
            Asset.objects.update_or_create(
                code=a["code"],
                defaults=a
            )
        self.stdout.write(self.style.SUCCESS("Assets initialisés"))

