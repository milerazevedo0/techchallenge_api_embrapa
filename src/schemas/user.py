from pydantic import BaseModel, validator, Field, field_validator
import re

def has_letter(s: str) -> bool:
    return bool(re.search(r"[A-Za-z]", s))

def has_number(s: str) -> bool:
    return bool(re.search(r"\d", s))

def has_special_char(s: str) -> bool:
    return bool(re.search(r"[^A-Za-z0-9]", s))

class UserCreate(BaseModel):
    user: str = Field(..., min_length=1, description="Recebe o nome de usuário para criação em sistema.")
    password: str = Field(..., min_length=6, description="Recebe a senha do usuário, que deve conter no minimo 6 digitos, ao menos 1 letra, 1 número e 1 caractere especial.")

    @field_validator('user')
    @classmethod
    def user_cannot_be_empty(cls, v):
        if not v.strip():
            raise ValueError('O usuário não pode ser vazio ou conter apenas espaços.')
        return v
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if not (has_letter(v) and has_number(v) and has_special_char(v)):
            raise ValueError('A senha deve conter pelo menos uma letra, um número e um caractere especial.')
        return v

class UserLogin(BaseModel):
    user: str = Field(..., description="Recebe o usuário para logar na aplicação")
    password: str = Field(..., description="Recebe a senha para realizar o login na aplicação")

    @field_validator('user', 'password')
    @classmethod
    def user_cannot_be_empty(cls, v):
        if not v.strip():
            raise ValueError('O usuário não pode ser vazio ou conter apenas espaços.')
        return v