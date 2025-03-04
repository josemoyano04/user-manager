
from models.user_db import UserDB
from fastapi import APIRouter, Body
from controllers import db_controllers as c
from models.request.add_user_request import AddUserRequest
from models.request.delete_user_request import DeleteUserRequest
from models.request.update_user_request import UpdateUserRequest

router  = APIRouter(prefix= "/user")

@router.post("/register")
async def register(request: AddUserRequest):
    res = await c.add_user_controller(request)
    return res

@router.delete("/delete")
async def delete(request: DeleteUserRequest):
    res = await c.delete_user_controller(request)
    return res

@router.put("/update")
async def update(request: UpdateUserRequest):
    res = await c.update_user_controller(request)
    return res
