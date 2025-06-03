import datetime
from enum import Enum
import requests
from sqlalchemy.orm import Session
from src.db.models.exportation import ExportationModel
from src.db.session import get_db
from src.scraping.scraping_exportation import Exportation, parse_exportation


class Suboption(str, Enum):
    subopt_01 = "Vinhos de mesa"
    subopt_02 = "Espumantes"
    subopt_03 = "Uvas frescas"
    subopt_04 = "Suco de uva"

def handle_exportation(year: int, suboption: Suboption | None, item: str | None) -> list[Exportation]:
    two_hours_ago = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=2)
    db: Session = next(get_db())
    query = db.query(ExportationModel)
    if year:
        query = query.filter(ExportationModel.year == year)
    if suboption:
        query = query.filter(ExportationModel.suboption == suboption.value)
    if item:
        query = query.filter(ExportationModel.item == item)
    existing_data = query.filter(ExportationModel.importedAt.__lt__(two_hours_ago)).all()

    if not existing_data:
        for sub in Suboption:
            if suboption and sub != suboption:
                continue

            url = f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_06&subopcao={sub.name}'
            response = requests.get(url)
            if response.status_code != 200:
                raise Exception(f"Failed to fetch data for year {year} and item {item}. Status code: {response.status_code}")
            scraped_data = parse_exportation(response.text)

            db.query(ExportationModel).filter(ExportationModel.year == year).filter(ExportationModel.suboption == sub.value).delete()
            db.commit()

            for exportation in scraped_data:
                db_exportation = ExportationModel(
                    year=year,
                    suboption=suboption,
                    country=exportation.country,
                    quantity=exportation.quantity,
                    value=exportation.value
                )
                db.add(db_exportation)

        try:
            db.commit()
        except Exception as e: 
            db.rollback()
            raise Exception(f"Error saving exportation data: {str(e)}")
        
    read = query.all()
    if not read:
        return []
    return [Exportation(
        suboption=str(exportation.suboption),
        country=str(exportation.country),
        quantity=int(exportation.quantity),
        value=int(exportation.value)
    ) for exportation in read]