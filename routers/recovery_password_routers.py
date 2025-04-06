from fastapi import APIRouter
from connections.db_connection import db_conn_libsql_client
from controllers import recovery_user_password_controller as c

router = APIRouter(tags=["Recovery password methods"], prefix="/recoveryPassword")
DB_CONN = db_conn_libsql_client()


@router.post("/sendEmail")
async def send_email(recovery_password_request: c.RecoveryPasswordRequest):
    res = await c.generate_and_send_code_controller(db_conn= DB_CONN, 
                                              recovery_password_request= recovery_password_request)

    return res

@router.post("/validateCode")
async def validate_code(validate_code_request: c.ValidateRecoveryCodeRequest):
    res = await c.validate_code_controller(db_conn= DB_CONN,
                                     validate_code_request= validate_code_request)
    
    return res