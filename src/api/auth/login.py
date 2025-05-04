from fastapi import APIRouter, HTTPException
from src.schemas.user import UserLogin
from src.crud.user import authenticate_user
from src.core.security import create_access_token

router = APIRouter()

@router.post('/login', 
             summary="Realiza o login do usuário",
             description="Recebe o nome de usuário e senha e valida se o mesmo já existe. Caso já exista, realiza o login e retorna um Token.",
             responses={
                 200: {"description": "Login realizado com sucesso"},
                 401: {"description": "Usuário ou senha inválidos."}
             })
async def login(user:UserLogin):
    db_user = authenticate_user(user.user, user.password)
    if not db_user:
        raise HTTPException(status_code=400, detail="Credenciais inválidas")
    token = create_access_token({"sub": db_user.user})
    return {"access_token": token, "token_type": "bearer"}