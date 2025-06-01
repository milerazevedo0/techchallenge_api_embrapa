# type: ignore
from bs4 import BeautifulSoup

class Exportation:
    country: str
    quantity: int
    value: int
    option: str

def parse_exportation(content: str) -> list[Exportation]:
    exportations: list[Exportation] = []

    soup = BeautifulSoup(content, 'html.parser')
    option_button = soup.find(id='btn1_active')
    table = soup.find('table', class_='tb_dados')
    tbody = table.find('tbody')

    for row in tbody.find_all('tr'):
        cells = row.find_all('td')
        if cells and len(cells) >= 3:
            exportation = Exportation()
            exportation.option = option_button.text.strip()
            exportation.country = cells[0].text.strip()

            quantity_text = cells[1].text.strip().replace('.', '')
            if quantity_text == '-':
                exportation.quantity = 0
            else:
                try:
                    exportation.quantity = int(quantity_text)
                except ValueError:
                    exportation.quantity = 0
            
            value_text = cells[2].text.strip().replace('.', '')
            if value_text == '-':
                exportation.value = 0
            else:
                try:
                    exportation.value = int(value_text)
                except ValueError:
                    exportation.value = 0

            exportations.append(exportation)

    return exportations