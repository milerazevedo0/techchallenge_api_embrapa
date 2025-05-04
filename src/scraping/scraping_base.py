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

    # Procura a tabela (geralmente a primeira grande)
    tabela = soup.find('table', {'class': 'tb_base tb_dados'})
    if not tabela:
        raise HTTPException(
            status_code=404,
            detail="Tabela de dados não encontrada!"
        )

    headers = []
    linhas_json = []

    # Pega os cabeçalhos
    for th in tabela.find_all('th'):
        headers.append(th.get_text(strip=True))

    # Pega as linhas
    for row in tabela.find_all('tr')[1:]:
        cols = row.find_all(['td'])
        if not cols:
            continue
        dados = [col.get_text(strip=True) for col in cols]
        linha_dict = dict(zip(headers, dados))
        linhas_json.append(linha_dict)

    return linhas_json





# def scrape_table(ano, opcao, subopcao=None):
#     url = f"http://vitibrasil.cnpuv.embrapa.br/index.php"
#     params = {
#         'ano': ano,
#         'opcao': opcao
#     }

#     if subopcao:
#         params.update(subopcao)

#     response = requests.get(url, params=params)
#     response.encoding = 'utf-8'
#     soup = BeautifulSoup(response.text, 'html.parser')

#     # Procura a tabela (geralmente a primeira grande)
#     tabela = soup.find('table', {'class': 'tb_base tb_dados'})
#     if not tabela:
#         return {"erro": "Tabela não encontrada"}

#     headers = []
#     linhas_json = []

#     # Pega os cabeçalhos
#     for th in tabela.find_all('th'):
#         headers.append(th.get_text(strip=True))

#     # Pega as linhas
#     for row in tabela.find_all('tr')[1:]:
#         cols = row.find_all(['td'])
#         if not cols:
#             continue
#         dados = [col.get_text(strip=True) for col in cols]
#         linha_dict = dict(zip(headers, dados))
#         linhas_json.append(linha_dict)

#     # return tabela
#     return linhas_json

# Exemplo de uso
# dados_2022 = scrape_table(2000, 'opt_03', {"subopcao": "subopt_02"})
# print(json.dumps(dados_2022, ensure_ascii=False, indent=2))
# print(dados_2022)
