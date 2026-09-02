from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm

from src.main.server.database import Session
from src.main.models.user import User
from src.main.validators.user import TokenResponse, UserResponse
from src.main.core.security import verifyPassword, createAcessToken, getCurrentUser

authRoutes = APIRouter(prefix="/auth", tags=["Authenticate"])

@authRoutes.post("/login", response_model=TokenResponse)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: Session):
    try: 
        saramInt = int(form_data.username)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O campo username (SARAM) deve ser um número inteiro.",
        )

    query = select(User).where(User.saram == saramInt)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    # Prevenção contra enumeração de usuários (mesma mensagem de erro)
    if not user or not verifyPassword(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Saram ou senha icorretos.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário desativado pelo administrador"
        )

    token_data = {
        "sub": str(user.saram),
        "user_id": user.id,
        "admin": user.admin,
        "name": f"{user.first_name} {user.last_name}",
    }

    token = createAcessToken(token_data)
    return {"access_token": token, "token_type": "bearer"}

@authRoutes.get("/me", response_model=UserResponse)
async def getMe(current_user: Annotated[User, Depends(getCurrentUser)]):
    return current_user
   

    