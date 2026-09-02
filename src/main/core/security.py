import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy import select

from dotenv import load_dotenv

from src.main.server.database import Session
from src.main.models.user import User


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITH")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACESS_TOKEN_EXPIRE_MINUTES", 480))

oauth2Scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# Criação e validação de senha HASH
def gerateHashPassword(password_clear: str) -> str:
    """transforma a senha em texto puro em um hash seguro"""
    pwd_bytes = password_clear.encode('utf-8')[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')

def verifyPassword(password_clear: str, password_hash: str) -> str:
    """Verifica se a senha enviada corresponde ao hash salvo no banco"""
    pwd_bytes = password_clear.encode('utf-8')[:72]
    hash_bytes = password_hash.encode('utf-8')
    return bcrypt.checkpw(pwd_bytes, hash_bytes)

# --- TOKEN JWT ---
def createAcessToken(data: dict, expires_delta: timedelta | None = None) -> str:
    payload = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta if expires_delta else timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    payload.update({"exp": expire, "iat": datetime.now(timezone.utc)})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decodeAcessToken(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Token expirado. Faça login novamente",
            headers = {"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Token Inválido",
            headers = {"WWW-Authenticate": "Bearer"}
        )

# --- GUARDS / DEPENDÊNCIAS DE AUTENTICAÇÃO ---
async def getCurrentUser(
        token: Annotated[str, Depends(oauth2Scheme)],
        session: Session,
) -> User:
    payload = decodeAcessToken(token)
    saramStr: str | None = payload.get("sub")

    if saramStr is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas no token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    query = select(User).where(User.saram == int(saramStr))
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )

    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo",
        )

    return user


async def requireAdmin(
    current_user: Annotated[User, Depends(getCurrentUser)],
) -> User:
    if not current_user.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito apenas para administradores.",
        )
    return current_user


