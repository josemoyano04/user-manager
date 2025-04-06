from pydantic import BaseModel, Field, EmailStr

class UpdatedPasswordRequest(BaseModel):
    email: EmailStr = Field(..., description="Email del usuario")
    new_password: str = Field(..., description="Nueva contraseña del usuario")
