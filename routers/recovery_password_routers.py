from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from connections.db_connection import db_conn_libsql_client
from controllers import recovery_user_password_controller as c
from services.auth_services import oauth2_schema

router = APIRouter(tags=["Recovery password methods"], prefix="/recovery-password")
DB_CONN = db_conn_libsql_client()


@router.post("/request")
async def send_email(recovery_password_request: c.RecoveryPasswordRequest):
    res = await c.generate_and_send_code_controller(db_conn= DB_CONN, 
                                              recovery_password_request= recovery_password_request)

    return res

@router.post("/verify-code")
async def validate_code(validate_code_request: c.ValidateRecoveryCodeRequest):
    res = await c.validate_code_controller(db_conn= DB_CONN,
                                     validate_code_request= validate_code_request)
    
    return res

@router.post("/reset")
async def update_password(updated_password_request: c.UpdatedPasswordRequest,
                           token: str = Depends(oauth2_schema)):
    res = await c.updated_password_controller(db_conn= DB_CONN,
                                             updated_password_request= updated_password_request,
                                             token= token)
    return res