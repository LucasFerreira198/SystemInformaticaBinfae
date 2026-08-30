from pydantic import BaseModel, Field
from typing import Optional

class userSchema(BaseModel):
    saram: int = Field(..., description="Número de saram valido")
    first_name: str = Field(..., min_length=3)
    last_name: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6, description="Minimo de 6 caracteres")
    active: Optional[bool] = Field(default=True)
    admin: Optional[bool] = Field(default=False)

    model_config = {
        "from_attributes": True
    }

   