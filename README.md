# 📊 Embrapa Scraper API

Esta aplicação fornece uma API REST desenvolvida com **FastAPI** que realiza raspagem de dados diretamente do site oficial da **Embrapa - Vitivinicultura Brasileira** (http://vitibrasil.cnpuv.embrapa.br/). O projeto permite consultar dados históricos de produção, exportação, processamento de uvas e mais — diretamente via requisições HTTP autenticadas por **JWT**.

---

## 🚀 Funcionalidades

- 🔐 Registro e login com autenticação JWT
- 🕵️‍♂️ Scraping dinâmico por ano, aba (`opcao`) e sub-aba (`subopcao`)
- 🔄 Retorno dos dados em **JSON estruturado**
- ✅ Proteção com token JWT para todas as rotas de scraping
- 📦 Organização com FastAPI Routers

---

## 🛠️ Tecnologias

- Python 3.12+
- FastAPI
- BeautifulSoup (bs4)
- Uvicorn
- Requests
- SQLAlchemy + SQLite/MySQL (dependendo da sua config)
- JWT (via `python-jose`)
- Pydantic
- Poetry

---


## 📥 Instalação
Pré-requisitos: \
Python 3.12+ \
Poetry (gerenciador de pacotes)

Passos para Instalação

Clone o repositório: \
git clone https://github.com/milerazevedo0/tech_challenge_embrapa_api/

cd tech_challenge_embrapa_api

Instale as dependências com Poetry: \
poetry install

Ative o ambiente virtual: \
poetry shell

Inicie o servidor de desenvolvimento: \
uvicorn app:app --reload

A API estará disponível em http://localhost:8000

## 🔍 Como Usar
Após iniciar o servidor, acesse:

Swagger UI: http://localhost:8000/docs \
ReDoc: http://localhost:8000/redoc

🔐 Fluxo de Autenticação JWT
A API utiliza autenticação JWT (JSON Web Token) para proteger os endpoints de scraping.

🧾 1. Criar usuário
Faça um POST para /auth/signup com os dados:
{
  "username": "seu_usuario",
  "password": "sua_senha"
}

🔑 2. Fazer login
Faça um POST para /auth/login com os mesmos dados:
{
  "username": "seu_usuario",
  "password": "sua_senha"
}

💡 A resposta será um token JWT:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}

📋 3. Autenticar nas rotas de scraping \
Copie o token retornado no login e informe no cabeçalho Authorization das demais rotas assim:
Authorization: Bearer SEU_TOKEN_JWT

Você pode testar diretamente no Swagger UI:

Acesse http://localhost:8000/docs

Clique em Authorize no topo

Digite Bearer SEU_TOKEN_AQUI

Teste as rotas com autenticação ativada

## 📥 Rotas de Scraping
🔎 /scrape/processing
Retorna dados da aba de processamento, exigindo ano e subopção:

GET /scrape/processing?ano=2022&subopcao=subopt_02

ano: entre 1970 e 2023

subopcao:

subopt_01 → viníferas

subopt_02 → americanas e híbridas

subopt_03 → uvas de mesa

subopt_04 → sem classificação

## 📌 Observações
A raspagem depende da estrutura atual do site da Embrapa, que pode mudar.

O projeto pode ser adaptado para novas abas (opcao) e novas subcategorias (subopcao).

O retorno é convertido para JSON estruturado com cabeçalhos e linhas mapeadas corretamente.

## 🤝 Contribuições
Contribuições são bem-vindas! Você pode abrir uma issue, forkear o repositório ou abrir um PR com sugestões ou melhorias.

## 📄 Licença
Este projeto é open-source e licenciado sob a MIT License.

## 🙋‍♂️ Dúvidas?
Se tiver dúvidas ou precisar de ajuda para configurar ou adaptar novas rotas, fique à vontade para abrir uma issue ou me procurar.