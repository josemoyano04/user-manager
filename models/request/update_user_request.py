from pydantic import BaseModel
from models.user_db import UserDB

class UpdateUserRequest(BaseModel):
    username: str
    updated_user: UserDB