from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from typing import Annotated


from src.main.validators.user import userCreateSchema
from src.main.server.database import Session
from src.main.models.user import User
from src.main.core.security import gerateHashPassword, getCurrentUser, requireAdmin


userRoutes = APIRouter(prefix="/users", tags=["Users"])

@userRoutes.post("/createUser")
async def createUser(user_schema: userCreateSchema, session: Session):
    # Consulta assíncrona usando select()
    query = select(User).where(User.saram == user_schema.saram)
    result = await session.execute(query)
    user_exists = result.scalar_one_or_none()

    # validação de duplicidade
    if user_exists:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST, 
            detail = "Saram do usuário já cadastrado"
            )
    
    password_crypt = gerateHashPassword(user_schema.password)

    new_user = User(
        saram = user_schema.saram,
        first_name = user_schema.first_name,
        last_name = user_schema.last_name,
        password = password_crypt,
        active = user_schema.active,
        admin = user_schema.admin
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return {
        "message": f"Usuário {new_user.first_name} Cadastrado com sucesso",
        "id": new_user.id,
        "saram": new_user.saram
    }

@userRoutes.get("/listUsers")
async def listUsers(session: Session, _: Annotated[User, Depends(requireAdmin)]):
    query = select(User)
    result = await session.execute(query)
    users = result.scalars().all()

    return [
        {
            "saram": u.saram,
            "first_name": u.first_name,
            "last_name": u.last_name,
            "active": u.active,
            "admin": u.admin,
        }
        for u in users
    ]



