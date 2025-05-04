from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from src.scraping.scraping_base import scrape_table
from src.db.models.user import User
from src.core.dependencies import get_current_user
from enum import Enum
from typing import Optional

router = APIRouter()

class SubopcaoProcessing(str, Enum):
    subopt_01 = "viniferas"
    subopt_02 = "americanas e hibridas"
    subopt_03 = "uvas de mesa"
    subopt_04 = "sem classificacao"

@router.get('/scrape/processing', 
             summary="Realiza a raspagem da aba de processamento",
             description="Realiza a raspagem da aba de processamento, com ou sem subopções e retorna os dados contidos na tabela selecionada.",
             responses={
                 200: {"description": "Raspagem realizada com sucesso"},
                 400: {"description": "Parâmetros inválidos"},
                 401: {"description": "Parametros inconsistentes."},
                 404: {"description": "Tabela não encontrada"},
                 503: {"description": "Erro ao acessar a fonte de dados"},
             })
async def processing(
    ano: int = Query(..., ge=1970, le=2023, description="Informe o ano entre 1970 e 2023"), 
    subopcao: Optional[SubopcaoProcessing] = Query(None), 
    current_user: User = Depends(get_current_user)
    ):
    subopcao_dict = {"subopcao": subopcao.name} if subopcao else None
    dados = scrape_table(ano, 'opt_03', subopcao=subopcao_dict)
    return JSONResponse(content=dados)