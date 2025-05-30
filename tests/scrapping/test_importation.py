from src.scraping.scraping_importation import parse_importation

def test_importation_parsing():
    with open('tests/scrapping/stubs/importacao.html', 'r', encoding='utf-8') as file:
        content = file.read()
        importations = parse_importation(content)

        assert len(importations) >= 5

        assert importations[0].country == 'Africa do Sul'
        assert importations[0].quantity == 658238
        assert importations[0].value == 2133775
        assert importations[0].option == 'Vinhos de mesa'