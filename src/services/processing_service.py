import datetime
from enum import Enum
import requests
from sqlalchemy.orm import Session
from src.db.models.processing import ProcessingModel
from src.db.session import get_db
from src.scraping.scraping_processing import Processing, parse_processing

class Suboption(str, Enum):
    subopt_01 = "Viníferas"
    subopt_02 = "Americanas e híbridas"
    subopt_03 = "Uvas de mesa"
    subopt_04 = "Sem classificação"

def handle_processing(year: int, suboption: Suboption | None, item: str | None) -> list[Processing]:
    two_hours_ago = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=2)
    db: Session = next(get_db())
    query = db.query(ProcessingModel)
    if year:
        query = query.filter(ProcessingModel.year == year)
    if suboption:
        query = query.filter(ProcessingModel.suboption == suboption.value)
    if item:
        query = query.filter(ProcessingModel.item == item)
    existing_data = query.filter(ProcessingModel.importedAt.__lt__(two_hours_ago)).all()

    if not existing_data:
        for sub in Suboption:
            if suboption and sub != suboption:
                continue

            url = f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_03&subopcao={sub.name}'
            response = requests.get(url)
            if response.status_code != 200:
                raise Exception(f"Failed to fetch data for year {year} and item {item}. Status code: {response.status_code}")
            scraped_data = parse_processing(response.text)

            db.query(ProcessingModel).filter(ProcessingModel.year == year).filter(ProcessingModel.suboption == sub.value).delete()  # Clear existing data for the year/item if any
            db.commit()  # Commit the deletion before adding new data
            # Convert and save to database
            for processing in scraped_data:
                db_processing = ProcessingModel(
                    year=year,
                    suboption=suboption,
                    item=processing.item,
                    subitem=processing.subitem,
                    quantity=processing.quantity
                )
                db.add(db_processing)

        try:
            db.commit()
        except Exception as e:
            db.rollback()
            raise Exception(f"Error saving processing data: {str(e)}")
        
    read = query.all()
    if not read:
        return []
    return [Processing(
        suboption=str(p.suboption),
        item=str(p.item),
        subitem=str(p.subitem),
        quantity=int(p.quantity)
    ) for p in read]