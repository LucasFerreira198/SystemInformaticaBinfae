from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.main.server.database import getSession
from src.main.validators.user import userSchema

authRoutes = APIRouter(tags=["Auth"])


   

    