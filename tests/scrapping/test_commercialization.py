from src.scraping.scraping_commercialization import parse_commercialization

def test_commercialization_parsing():
    with open('tests/scrapping/stubs/comercializacao.html', 'r', encoding='utf-8') as file:
        content = file.read()
        commercializations = parse_commercialization(content)

        assert len(commercializations) >= 5

        assert commercializations[0].item == 'VINHO DE MESA'
        assert commercializations[0].subitem == 'Tinto'
        assert commercializations[0].quantity == 165097539

        assert commercializations[5].item == 'VINHO FINO DE MESA'
        assert commercializations[5].subitem == 'Branco'
        assert commercializations[5].quantity == 4924121