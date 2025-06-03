# type: ignore
from bs4 import BeautifulSoup
from pydantic import BaseModel

class Processing(BaseModel):
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
                quantity_value = 0
                quantity_text = row.find_all('td')[-1].text.strip()
                try:
                    quantity_value = int(quantity_text.replace('.', ''))
                except (ValueError, AttributeError):
                    quantity_value = 0

                processing = Processing(
                    suboption=suboption_text, 
                    subitem=subitem_cell.text.strip(), 
                    item=current_item, 
                    quantity=quantity_value)
                
                processing_list.append(processing)

    return processing_list