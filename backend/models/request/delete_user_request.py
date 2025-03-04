from pydantic import BaseModel

class DeleteUserRequest(BaseModel):
    username: str