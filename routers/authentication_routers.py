from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from controllers import auth_controller as at
from services.auth_services import oauth2_schema
from models.user_db import UserDB


router = APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl= "/login")


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    res = await at.login_for_access_token_controller(form_data)
    return res