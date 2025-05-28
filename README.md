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
Pré-requisitos: 
- Python 3.12+ 
- Poetry 2+

Passos para Instalação

1. Clone o repositório: 

```sh
git clone https://github.com/milerazevedo0/tech_challenge_embrapa_api/`
cd tech_challenge_embrapa_api
```

2. Instale as dependências com Poetry: 

```sh
poetry install
```

3. Ative o ambiente virtual:

```sh
poetry shell
```

4. Inicie o servidor de desenvolvimento:

```sh
uvicorn app:app --reload
```

A API estará disponível em http://localhost:8000

## 🔍 Como Usar
Após iniciar o servidor, acesse:

Swagger UI: http://localhost:8000/docs \
ReDoc: http://localhost:8000/redoc

🔐 Fluxo de Autenticação JWT
A API utiliza autenticação JWT (JSON Web Token) para proteger os endpoints de scraping.

### 🧾 1. Criar usuário
Faça um POST para `/auth/signup` com os dados:

```json
{
  "username": "seu_usuario",
  "password": "sua_senha"
}
```

### 🔑 2. Fazer login
Faça um POST para `/auth/login` com os mesmos dados:

```json
{
  "username": "seu_usuario",
  "password": "sua_senha"
}
```

💡 A resposta será um token JWT:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 📋 3. Autenticar nas rotas de scraping
Copie o token retornado no login e informe no cabeçalho Authorization das demais rotas assim:
`Authorization: Bearer SEU_TOKEN_JWT`

Você pode testar diretamente no Swagger UI:

 1. Acesse http://localhost:8000/docs
 2. Clique em Authorize no topo
 3. Digite Bearer SEU_TOKEN_AQUI

Teste as rotas com autenticação ativada

## 📌 Observações
A raspagem depende da estrutura atual do site da Embrapa, que pode mudar.

## 📄 Licença
Este projeto é open-source e licenciado sob a MIT License.

## 🙋‍♂️ Dúvidas?
Se tiver dúvidas ou precisar de ajuda para configurar ou adaptar novas rotas, fique à vontade para abrir uma issue ou me procurar.