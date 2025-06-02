import requests
from sqlalchemy.orm import Session
from src.db.models.production import ProductionModel
from src.db.session import get_db
from src.scraping.scraping_production import Production, parse_production
from typing import List

def handle_production(year: int, item: str | None) -> List[Production]:
    # Query existing data
    db: Session = next(get_db())
    query = db.query(ProductionModel)
    if year:
        query = query.filter(ProductionModel.year == year)
    if item:
        query = query.filter(ProductionModel.item == item)
    existing_data = query.all()
    
    # If no data exists, scrape and save
    if not existing_data:
        url = f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_02'
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data for year {year} and item {item}. Status code: {response.status_code}")
        scraped_data = parse_production(response.text)
        
        # Convert and save to database
        for production in scraped_data:
            db_production = ProductionModel(
                year=year,
                item=production.item,
                subitem=production.subitem,
                quantity=production.quantity
            )
            db.add(db_production)
        
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            raise Exception(f"Error saving production data: {str(e)}")
    
    # Convert DB models to Production DTOs
    read = query.all()
    if not read:
        return []
    return [Production(
        item=str(p.item), 
        subitem=str(p.subitem), 
        quantity=int(p.quantity), 
        year=int(p.year)) for p in read]