import requests
from bs4 import BeautifulSoup
from fastapi import HTTPException

def scrape_table(ano, opcao, subopcao=None):
    url = "http://vitibrasil.cnpuv.embrapa.br/index.php"
    params = {
        'ano': ano,
        'opcao': opcao
    }

    if subopcao:
        params.update(subopcao)

    try:
        response = requests.get(url, params=params, timeout=10)
        response.encoding = 'utf-8'
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=503,
            detail=f"Erro ao acessar o site da Embrapa. Tente novamente mais tarde. Detalhes técnicos: {str(e)}"
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=503,
            detail=f"Site retornou status inesperado: {response.status_code}"
        )

    soup = BeautifulSoup(response.text, 'html.parser')

    tabela = soup.find('table', {'class': 'tb_base tb_dados'})
    if not tabela:
        raise HTTPException(
            status_code=404,
            detail="Tabela de dados não encontrada!"
        )

    headers = []
    linhas_json = []

    for th in tabela.find_all('th'):
        headers.append(th.get_text(strip=True))

    for row in tabela.find_all('tr')[1:]:
        cols = row.find_all(['td'])
        if not cols:
            continue
        dados = [col.get_text(strip=True) for col in cols]
        linha_dict = dict(zip(headers, dados))
        linhas_json.append(linha_dict)

    return linhas_json