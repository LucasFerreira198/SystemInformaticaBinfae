from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from typing import Annotated


from src.main.validators.user import userCreateSchema, UserResponse, UserUpdateSchema
from src.main.server.database import Session
from src.main.models.user import User
from src.main.core.security import gerateHashPassword, getCurrentUser, requireAdmin


userRoutes = APIRouter(prefix="/users", tags=["Users"])


# Crud C- Create
@userRoutes.post("/createUser", response_model=UserResponse)
async def createUser(user_schema: userCreateSchema, session: Session):
    '''Criação de usuários '''
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

    return new_user
#crud r- read all
@userRoutes.get("/listUsers")
async def listUsers(session: Session, _: Annotated[User, Depends(requireAdmin)]):
    """Listar todos os usuários da aplicação"""
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

#Crud r- read for saram
@userRoutes.get("/{saram}", response_model=UserResponse)
async def getUser(
    saram: int,
    session: Session,
    _: Annotated[User, Depends(requireAdmin)]
):
    """Listar as informações de um usuário especifico pelo saram"""
    query = select(User).where(User.saram == saram)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Militar não encontrado"
        )
    
    return user

# Crud u- Update
@userRoutes.patch("/update/{saram}", response_model=UserResponse)
async def updateUser(
    saram: int,
    user_data: UserUpdateSchema,
    session: Session,
    _: Annotated[User, Depends(requireAdmin)]
):
    """Editar e atualizar as informações de um usuário"""
    query = select(User).where(User.saram == saram)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Militar não econtrado"
        )

    update_data = user_data.model_dump(exclude_unset=True)

    if "password" in update_data:
        update_data["password"] = gerateHashPassword(update_data["password"])

    for key, value in update_data.items():
        setattr(user, key, value)


    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user

#Crud D- Delete
@userRoutes.delete("/delete/{saram}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteUser(
    saram: int,
    session: Session,
    _: Annotated[User, Depends(requireAdmin)]
):
    """Deletar usuários"""
    query = select(User).where(User.saram == saram)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Militar não encontrado"
        )

    await session.delete(user)
    await session.commit()

    return None