from pydantic import BaseModel, EmailStr

class ValidateRecoveryCodeRequest(BaseModel):
    code: str
    user_email: EmailStr