from src.scraping.scraping_exportation import parse_exportation


def test_exportation_parsing():
    with open('tests/scrapping/stubs/exportacao.html', 'r', encoding='utf-8') as file:
        content = file.read()
        exportations = parse_exportation(content)

        assert len(exportations) >= 5

        assert exportations[1].country == 'África do Sul'
        assert exportations[1].quantity == 103
        assert exportations[1].value == 1783
        assert exportations[1].option == 'Vinhos de mesa'