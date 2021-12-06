from bs4 import BeautifulSoup


def find_price_values(response) -> (float, str):
    price_values = []

    page_soup = BeautifulSoup(response, "html.parser")
    price_values_scraper = page_soup.find('div', class_='col-6')

    for elem in price_values_scraper:
        price_values.append(elem.text)

    price_usd = float(price_values[3].split()[0][1:])
    price_increase = price_values[3].split()[4][1:-1]
    return price_usd, price_increase


def find_market_cap(response) -> float:
    button_values = []

    page_soup = BeautifulSoup(response, "html.parser")
    buttons = page_soup.find_all('button')

    for elem in buttons:
        button_values.append(elem.text)

    market_cap = float(button_values[2][2:].replace(',', ''))
    return market_cap
