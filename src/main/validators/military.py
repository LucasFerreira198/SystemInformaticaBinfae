from pydantic import BaseModel, Field
from typing import Optional

# --- Schema para Criação (POST) ---
class MilitaryCreateSchema(BaseModel):
    saram: int = Field(..., description="Número de SARAM (único para cada militar)")
    nome_completo: str = Field(..., min_length=5, description="Nome completo do militar")
    posto_graduacao: str = Field(..., description="Posto ou Graduação (ex: 3S, 2T, Cel)")
    nome_guerra: str = Field(..., min_length=2, description="Nome de guerra do militar")
    email: Optional[str] = Field(default=None, description="E-mail corporativo ou pessoal")
    celular: Optional[str] = Field(default=None, description="Número de celular com DDD")

# --- Schema para Atualização Parcial (PATCH) ---
class MilitaryUpdateSchema(BaseModel):
    nome_completo: Optional[str] = Field(default=None, min_length=5)
    posto_graduacao: Optional[str] = Field(default=None)
    nome_guerra: Optional[str] = Field(default=None, min_length=2)
    email: Optional[str] = Field(default=None)
    celular: Optional[str] = Field(default=None)

# --- Schema de Resposta (GET) ---
class MilitaryResponse(BaseModel):
    id: int
    saram: int
    nome_completo: str
    posto_graduacao: str
    nome_guerra: str
    email: Optional[str] = None
    celular: Optional[str] = None

    # Configuração vital para o Pydantic ler o modelo do SQLAlchemy
    model_config = {"from_attributes": True}