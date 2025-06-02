# type: ignore
from bs4 import BeautifulSoup

class Processing:
    suboption: str
    subitem: str
    item: str
    quantity: int

def parse_processing(content: str) -> list[Processing]:
    processing_list: list[Processing] = []

    soup = BeautifulSoup(content, 'html.parser')
    table = soup.find('table', class_='tb_dados')
    suboption_button = soup.find('button', id='btn1_active')
    suboption_text = suboption_button.text.strip() if suboption_button else ''

    if table:
        current_item = None
        for row in table.find_all('tr'):
            item_cell = row.find('td', class_='tb_item')
            if item_cell:
                current_item = item_cell.text.strip()
            
            subitem_cell = row.find('td', class_='tb_subitem')
            if subitem_cell and current_item:
                processing = Processing()
                processing.item = current_item
                processing.subitem = subitem_cell.text.strip()
                processing.suboption = suboption_text
                
                quantity_text = row.find_all('td')[-1].text.strip()
                try:
                    processing.quantity = int(quantity_text.replace('.', ''))
                except (ValueError, AttributeError):
                    processing.quantity = 0
                
                processing_list.append(processing)

    return processing_list