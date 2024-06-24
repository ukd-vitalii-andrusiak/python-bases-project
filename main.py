import requests
import json
from tabulate import tabulate


def get_exchange_rates():
    url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"

    try:
        response = requests.get(url)
        response.raise_for_status()
        exchange_rates = response.json()
        return exchange_rates
    except requests.exceptions.RequestException as e:
        print(f"Помилка отримання даних з НБУ: {e}")
    except json.JSONDecodeError:
        print("Помилка JSON відповіді")


def find_rate(currency_code, exchange_rates):
    if currency_code == "UAH":
        return 1.0
    for rate in exchange_rates:
        if rate['cc'] == currency_code:
            return rate['rate']
    print(f"Код валюти {currency_code} не знайдено в обмінних курсах.")


def convert_currency(from_currency, to_currency, amount, exchange_rates):
    from_rate = find_rate(from_currency, exchange_rates)
    to_rate = find_rate(to_currency, exchange_rates)

    if from_rate is None or to_rate is None:
        return None

    converted_amount = (amount * from_rate) / to_rate
    return converted_amount


def print_available_rates(exchange_rates):
    date = exchange_rates[0]["exchangedate"]
    table = [["Назва валюти", "Код валюти", f"Курс до гривні ({date})"]]
    for rate in exchange_rates:
        table.append([rate['txt'], rate['cc'], rate['rate']])
    table.append(["Українська гривня", "UAH", 1.0])
    ascii_table = tabulate(table, headers="firstrow", tablefmt="grid")
    print(ascii_table)


def main():
    exchange_rates = get_exchange_rates()

    if exchange_rates is None:
        print("Ми не отримали значення валют з НБУ.")
        return

    print_available_rates(exchange_rates)

    while True:
        from_currency = input(
            "Введіть код валюти з якої перерахувати (наприклад, USD, EUR) або 'exit' для виходу: ").strip().upper()
        if from_currency == 'EXIT':
            break
        to_currency = input("Введіть код валюти призначення (наприклад, USD, EUR): ").strip().upper()
        try:
            amount = float(input("Введіть суму для конвертації: ").strip())
        except ValueError:
            print("Невірна сума. Будь ласка, введіть числове значення.")
            continue

        result = convert_currency(from_currency, to_currency, amount, exchange_rates)
        if result is not None:
            print(f"{amount} {from_currency} дорівнює {result:.2f} {to_currency}")


if __name__ == "__main__":
    main()
