import datetime
import requests
from sqlalchemy.orm import Session
from src.db.models.comercialization import ComercializationModel
from src.db.session import get_db
from src.scraping.scraping_commercialization import Comercialization, parse_commercialization


def handle_commercialization(year: int, item: str | None) -> list[Comercialization]:
    # Query existing data
    two_hours_ago = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=2)
    db: Session = next(get_db())
    query = db.query(ComercializationModel)
    if year:
        query = query.filter(ComercializationModel.year == year)
    if item:
        query = query.filter(ComercializationModel.item == item)
    existing_data = query.filter(ComercializationModel.importedAt.__lt__(two_hours_ago)).all()

    if not existing_data:
        url = f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_04'
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data for year {year} and item {item}. Status code: {response.status_code}")
        scraped_data = parse_commercialization(response.text)

        db.query(ComercializationModel).filter(ComercializationModel.year == year).delete()
        db.commit()

        for commercialization in scraped_data:
            db_commercialization = ComercializationModel(
                year=year,
                item=commercialization.item,
                subitem=commercialization.subitem,
                quantity=commercialization.quantity
            )
            db.add(db_commercialization)

        try:
            db.commit()
        except Exception as e:
            db.rollback()
            raise Exception(f"Error saving commercialization data: {str(e)}")
        
    read = query.all()
    if not read:
        return []
    return [Comercialization(
        item=str(c.item), 
        subitem=str(c.subitem), 
        quantity=int(c.quantity)
    ) for c in read]