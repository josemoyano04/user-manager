from pydantic import BaseModel
from models.user_db import UserDB

class AddUserRequest(BaseModel):
    user: UserDB