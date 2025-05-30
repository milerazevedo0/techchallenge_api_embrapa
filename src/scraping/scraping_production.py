# type: ignore
from bs4 import BeautifulSoup

class Production:
    item: str
    subitem: str
    quantity: int

def parse_production(content:str) -> list[Production]:
    productions:list[Production] = []

    soup = BeautifulSoup(content, 'html.parser')
    table = soup.find('table', class_='tb_dados')

    if table:
        current_item = None
        for row in table.find_all('tr'):
            item_cell = row.find('td', class_='tb_item')
            if item_cell:
                current_item = item_cell.text.strip()
            
            subitem_cell = row.find('td', class_='tb_subitem')
            if subitem_cell and current_item:
                production = Production()
                production.item = current_item
                production.subitem = subitem_cell.text.strip()
                
                quantity_text = row.find_all('td')[-1].text.strip()
                try:
                    production.quantity = int(quantity_text.replace('.', ''))
                except (ValueError, AttributeError):
                    production.quantity = 0
                    
                productions.append(production)

    return productions