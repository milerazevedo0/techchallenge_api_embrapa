from src.scraping.scraping_production import parse_production

def test_production_parsing():
    with open('tests/scrapping/stubs/producao.html', 'r', encoding='utf-8') as file:
        content = file.read()
        productions = parse_production(content)

        assert len(productions) >= 5
        
        assert productions[0].item == 'VINHO DE MESA'
        assert productions[0].subitem == 'Tinto'
        assert productions[0].quantity == 139320884

        assert productions[6].item == 'SUCO'
        assert productions[6].subitem == 'Suco de uva integral'
        assert productions[6].quantity == 38122173