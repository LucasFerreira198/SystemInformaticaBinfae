from fastapi import APIRouter
from fastapi.responses import JSONResponse


authRoutes = APIRouter(tags=["Auth"])

@authRoutes.post("/")
async def create_user():
    """
    Rota de Teste
    """

    return JSONResponse(
        status_code=201, 
        content={
            "message": "Você acessou a rota padrão de autenticação",
            "Authenticate": False
        }
        )
    