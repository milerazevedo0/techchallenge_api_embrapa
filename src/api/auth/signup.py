from fastapi import APIRouter
from src.schemas.user import UserCreate
from src.crud.user import create_user

router = APIRouter()

@router.post("/signup", 
             summary="Realiza o cadastro do usuário",
             description="Rota responsável por realizar o cadastro do usuário, permitindo assim a autenticação posterioremente.",)
async def signup(user: UserCreate):
    user_db = create_user(user)
    return {"msg": f"Usuário {user_db.user} criado com sucesso!"}
