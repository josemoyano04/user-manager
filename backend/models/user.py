from pydantic import BaseModel, EmailStr

class User(BaseModel):
    full_name: str
    username: str
    email: EmailStr