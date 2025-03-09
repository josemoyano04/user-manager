from controllers import db_controllers as c
from fastapi import APIRouter, Body, Depends
from controllers import auth_controller as at
from services.auth_services import oauth2_schema
from models.request.add_user_request import AddUserRequest
from models.request.delete_user_request import DeleteUserRequest
from models.request.update_user_request import UpdateUserRequest

router  = APIRouter(prefix= "/user", tags= ["User methods"])


@router.get("/me")
async def get_users_me(token: str = Depends(oauth2_schema)):
    res = await at.get_current_user_controller(token)
    return res

@router.post("/register")
async def register(request: AddUserRequest):
    res = await c.add_user_controller(request)
    return res

@router.delete("/delete")
async def delete(request: DeleteUserRequest, token: str = Depends(oauth2_schema)):
    res = await c.delete_user_controller(request, token)
    return res


@router.put("/update")
async def update(request: UpdateUserRequest, token: str = Depends(oauth2_schema)):
    res = await c.update_user_controller(request, token)
    return res
