from forex_python.converter import CurrencyRates

class CurrencyConverter:
    def __init__(self):
        self.currency_rates = CurrencyRates()

    def convert(self, amount, from_currency, to_currency):
        converted_amount = self.currency_rates.convert(from_currency, to_currency, amount)
        return converted_amount

if __name__ == "__main__":
    converter = CurrencyConverter()

    amount = 1
    from_currency = "USD"
    to_currency = "UAH"

    converted_amount = converter.convert(amount, from_currency, to_currency)
    print(f"{amount} {from_currency} is equal to {converted_amount} {to_currency}")
