from pydantic import BaseModel, Field
from typing import Optional

# -- Criação de Usuário ---
class userCreateSchema(BaseModel):
    saram: int = Field(..., description="Número de saram valido")
    first_name: str = Field(..., min_length=3)
    last_name: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6, description="Minimo de 6 caracteres")
    active: Optional[bool] = Field(default=True)
    admin: Optional[bool] = Field(default=False)

    model_config = {
        "from_attributes": True
    }


# --- Login ___
class LoginSchema(BaseModel):
    saram: int = Field(..., description="Número de SARAM do militar")
    password: str = Field(..., min_length=1)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"

class UserResponse(BaseModel):
    id: int
    saram: int
    first_name: str
    last_name: str
    active: bool
    admin: bool

    model_config = {"from_attributes": True}
   