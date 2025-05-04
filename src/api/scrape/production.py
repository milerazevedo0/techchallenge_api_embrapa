from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from src.scraping.scraping_base import scrape_table
from src.db.models.user import User
from src.core.dependencies import get_current_user


router = APIRouter()

@router.get('/scrape/production', 
             summary="Realiza a raspagem da aba de produção",
             description="Realiza a raspagem da aba de produção, buscando a tabela e seus elementos. Retorna um JSON para consumo.",
             responses={
                 200: {"description": "Raspagem realizada com sucesso"},
                 400: {"description": "Parâmetros inválidos"},
                 401: {"description": "Parametros inconsistentes."},
                 404: {"description": "Tabela não encontrada"},
                 503: {"description": "Erro ao acessar a fonte de dados"},
             })
async def production(
    ano: int = Query(..., ge=1970, le=2023, description="Informe o ano entre 1970 e 2023"),
    current_user: User = Depends(get_current_user)
    ):
    dados = scrape_table(ano, 'opt_02')
    return JSONResponse(content=dados)