from fastapi import APIRouter, Depends, Query
from src.db.models.user import User
from src.core.dependencies import get_current_user
from src.services.commercialization_service import handle_commercialization


router = APIRouter()

@router.get('/commercialization', 
             summary="Realiza a raspagem da aba de comercialização",
             description="Realiza a raspagem da aba de comercialização, buscando a tabela e seus elementos. Retorna um JSON para consumo.",
             responses={
                 200: {"description": "Raspagem realizada com sucesso"},
                 400: {"description": "Parâmetros inválidos"},
                 401: {"description": "Parametros inconsistentes."},
                 404: {"description": "Tabela não encontrada"},
                 503: {"description": "Erro ao acessar a fonte de dados"},
             })
async def commercialization(
    ano: int = Query(..., ge=1970, le=2023, description="Informe o ano entre 1970 e 2023"),
    _: User = Depends(get_current_user)
    ):
    dados = handle_commercialization(year=ano, item=None)
    return dados