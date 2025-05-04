from sqlalchemy.orm import Session
from src.db.models.user import User
from src.db.session import get_db
from src.core.security import hash_password, verify_password
from fastapi import HTTPException

def create_user(user_data):
    db: Session = next(get_db())
    existing_user = db.query(User).filter(User.user == user_data.user).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Usuários já existente, por favor digite outro usuário.")
    user = User(user=user_data.user, hashed_password=hash_password(user_data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user 

def authenticate_user(user: str, password: str):
    db: Session = next(get_db())
    user = db.query(User).filter(User.user == user).first()
    if user and verify_password(password, user.hashed_password):
        return user
    return None
