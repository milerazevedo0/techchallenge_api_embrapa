# type: ignore
from bs4 import BeautifulSoup

class Importation:
    country: str
    quantity: int
    value: int
    option: str

def parse_importation(content: str) -> list[Importation]:
    importations: list[Importation] = []

    soup = BeautifulSoup(content, 'html.parser')
    option_button = soup.find(id='btn1_active')
    option_text = option_button.text.strip() if option_button else ''
    table = soup.find('table', class_='tb_dados')
    tbody = table.find('tbody')

    for row in tbody.find_all('tr'):
        cells = row.find_all('td')
        if cells and len(cells) >= 3:
            importation = Importation()
            importation.option = option_button.text.strip()
            importation.country = option_text

            quantity_text = cells[1].text.strip().replace('.', '')
            if quantity_text == '-':
                importation.quantity = 0
            else:
                try:
                    importation.quantity = int(quantity_text)
                except ValueError:
                    importation.quantity = 0
            
            value_text = cells[2].text.strip().replace('.', '')
            if value_text == '-':
                importation.value = 0
            else:
                try:
                    importation.value = int(value_text)
                except ValueError:
                    importation.value = 0

            importations.append(importation)

    return importations