from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from src.db.session import init_db
from src.api.auth import signup
from src.api.auth import login
from src.api.scrape import production, processing, commercialization, importation, export

app = FastAPI()

@app.on_event("startup")
def startup():
    init_db()

app.include_router(signup.router, prefix='/signup', tags=["Auth"])
app.include_router(login.router, prefix='/login', tags=["Auth"])
app.include_router(production.router, prefix='/producao', tags=['Scrape'])
app.include_router(processing.router, prefix='/processamento', tags=['Scrape'])
app.include_router(commercialization.router, prefix='/comercializacao', tags=['Scrape'])
app.include_router(importation.router, prefix='/importacao', tags=['Scrape'])
app.include_router(export.router, prefix='/exportacao', tags=['Scrape'])

@app.get("/", response_class=HTMLResponse)
async def home():
    html_content = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <title>Embrapa Scraper API</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 40px;
            }
            .container {
                background-color: #fff;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                max-width: 700px;
                margin: auto;
                text-align: center;
            }
            a {
                text-decoration: none;
                color: white;
                background-color: #007BFF;
                padding: 10px 20px;
                border-radius: 5px;
                margin-top: 20px;
                display: inline-block;
            }
            a:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚜 Embrapa Scraper API</h1>
            <p>
                Esta API realiza a raspagem de dados diretamente do portal da Embrapa Viticultura, 
                permitindo consultar dados históricos sobre produção, exportação, processamento de uvas e mais.
            </p>
            <p>
                Para testar as rotas e explorar as funcionalidades disponíveis, acesse a documentação interativa:
            </p>
            <a href="/docs" target="_blank">Abrir Swagger UI</a>
            <footer>
                <p>Acesse o repositório no <strong>Github</strong> • 
                <a href="https://github.com/murilobeltrame/tech-challenge-vitivinicultura-api" target="_blank">Ver no GitHub</a></p>
            </footer>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)