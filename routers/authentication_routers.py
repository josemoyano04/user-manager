from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from adapters.adapter_db_conn_libsql import AdapterDBConnLibsqlClient
from controllers import auth_controller as at
from models.user_db import UserDB
from utils.env_loader import EnvManager
from connections.db_connection import db_conn_libsql_client

#DATABASE CONNECTION CONSTANTS
ENV = EnvManager()

DATABASE_URL = ENV.get("PRODUCTION_DATABASE_URL")
DATABASE_AUTH_TOKEN = ENV.get("PRODUCTION_DATABASE_AUTH_TOKEN")

DB_CONN = db_conn_libsql_client()

router = APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl= "/login")


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    res = await at.login_for_access_token_controller(db_conn= DB_CONN, 
                                                     form_data= form_data)
    return res
