import datetime
from enum import Enum
import requests
from sqlalchemy.orm import Session
from src.db.models.importation import ImportationModel
from src.db.session import get_db
from src.scraping.scraping_importation import Importation, parse_importation


class Suboption(str, Enum):
    subopt_01 = "Vinhos de mesa"
    subopt_02 = "Espumantes"
    subopt_03 = "Uvas frescas"
    subopt_04 = "Uvas passas"
    subopt_05 = "Suco de uva"

def handle_importation(year: int, suboption: Suboption | None, item: str | None) -> list[Importation]:
    two_hours_ago = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=2)
    db: Session = next(get_db())
    query = db.query(ImportationModel)
    if year:
        query = query.filter(ImportationModel.year == year)
    if suboption:
        query = query.filter(ImportationModel.suboption == suboption.value)
    if item:
        query = query.filter(ImportationModel.item == item)
    existing_data = query.filter(ImportationModel.importedAt.__lt__(two_hours_ago)).all()

    if not existing_data:
        for sub in Suboption:
            if suboption and sub != suboption:
                continue

            url = f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_05&subopcao={sub.name}'
            response = requests.get(url)
            if response.status_code != 200:
                raise Exception(f"Failed to fetch data for year {year} and item {item}. Status code: {response.status_code}")
            scraped_data = parse_importation(response.text)

            db.query(ImportationModel).filter(ImportationModel.year == year).filter(ImportationModel.suboption == sub.value).delete()
            db.commit()

            for importation in scraped_data:
                db_importation = ImportationModel(
                    year=year,
                    suboption=suboption,
                    country=importation.country,
                    quantity=importation.quantity,
                    value=importation.value
                )
                db.add(db_importation)

        try:
            db.commit()
        except Exception as e: 
            db.rollback()
            raise Exception(f"Error saving importation data: {str(e)}")
        
    read = query.all()
    if not read:
        return []
    return [Importation(
        country=str(i.country),
        quantity=int(i.quantity),
        value=int(i.value),
        suboption=str(i.suboption)
    ) for i in read]