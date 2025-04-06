from fastapi import APIRouter, Depends
from controllers import auth_controller as at
from connections.db_connection import db_conn_libsql_client
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

DB_CONN = db_conn_libsql_client()

router = APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl= "/login")


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    res = await at.login_for_access_token_controller(db_conn= DB_CONN, 
                                                     form_data= form_data)
    return res
