from fastapi import APIRouter, Depends, Query
from src.db.models.user import User
from src.core.dependencies import get_current_user
from typing import Optional

from src.services.processing_service import Suboption, handle_processing

router = APIRouter()

@router.get('/processing', 
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
    subopcao: Optional[Suboption] = Query(None), 
    _: User = Depends(get_current_user)
    ):
    dados = handle_processing(year=ano, suboption=subopcao, item=None)
    return dados