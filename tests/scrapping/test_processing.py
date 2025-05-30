from src.scraping.scraping_processing import parse_processing

def test_processing_parsing():
    with open('tests/scrapping/stubs/processamento.html', 'r', encoding='utf-8') as file:
        content = file.read()
        processing = parse_processing(content)

        assert len(processing) >= 5
        
        assert processing[0].item == 'TINTAS'
        assert processing[0].subitem == 'Alicante Bouschet'
        assert processing[0].quantity == 4108858

        assert processing[2].item == 'TINTAS'
        assert processing[2].subitem == 'Aramon'
        assert processing[2].quantity == 0

        assert processing[6].item == 'TINTAS'
        assert processing[6].subitem == 'Barbera'
        assert processing[6].quantity == 35292