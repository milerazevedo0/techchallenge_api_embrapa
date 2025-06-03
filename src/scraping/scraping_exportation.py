# type: ignore
from bs4 import BeautifulSoup
from pydantic import BaseModel

class Exportation(BaseModel):
    country: str
    quantity: int
    value: int
    suboption: str

def parse_exportation(content: str) -> list[Exportation]:
    exportations: list[Exportation] = []

    soup = BeautifulSoup(content, 'html.parser')
    option_button = soup.find(id='btn1_active')
    table = soup.find('table', class_='tb_dados')
    tbody = table.find('tbody')

    for row in tbody.find_all('tr'):
        cells = row.find_all('td')
        if cells and len(cells) >= 3:
            quantity_value = 0
            quantity_text = cells[1].text.strip().replace('.', '')
            if quantity_text == '-':
                quantity_value = 0
            else:
                try:
                    quantity_value = int(quantity_text)
                except ValueError:
                    quantity_value = 0
            
            value_value = 0
            value_text = cells[2].text.strip().replace('.', '')
            if value_text == '-':
                value_value = 0
            else:
                try:
                    value_value = int(value_text)
                except ValueError:
                    value_value = 0

            exportation = Exportation(
                country=cells[0].text.strip(),
                quantity=quantity_value,
                value=value_value,
                suboption=option_button.text.strip() if option_button else ''
            )

            exportations.append(exportation)

    return exportations