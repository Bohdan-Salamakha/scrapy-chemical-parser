class CurrencyConverter:
    __CURRENCY_LIST = {"$": "USD"}

    @staticmethod
    def convert_currency(currency: str) -> str:
        return CurrencyConverter.__CURRENCY_LIST.get(currency)
