from fastapi import HTTPException, status, concurrency
from fastapi.responses import JSONResponse
from models.request.validate_code_request import ValidateRecoveryCodeRequest
from services.hashing_service import hashed_password
from errors.recovery_code_errors import ExpiredCodeError
from adapters.database_connection import DatabaseConnection
from services.db_services import get_user_by_email, update_user
from models.request.generate_code_request import RecoveryPasswordRequest
from services.password_recovery_email_sender import PasswordRecoveryEmailSender, PasswordRecoveryCodeManager

async def generate_and_send_code_controller(db_conn: DatabaseConnection, recovery_password_request: RecoveryPasswordRequest) -> JSONResponse:
    sender = PasswordRecoveryEmailSender()
    user = await get_user_by_email(db_conn= db_conn, 
                                   email= recovery_password_request.receiver_email,
                                   visible_password= True)
    
    if user is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail = {
                "status": "error",
                "message": "El email ingresado no esta registrado."
            })
    
    await concurrency.run_in_threadpool(sender.send_email_recovery_password,
                                        user.username,
                                        recovery_password_request.sender_email,
                                        recovery_password_request.password_email,
                                        recovery_password_request.receiver_email,
                                        recovery_password_request.email_template_html,
                                        recovery_password_request.custom_code)

    return JSONResponse(
            status_code = status.HTTP_200_OK, 
            content = {
                "status": "success",
                "message": "Código de recuperación enviado correctamente."
            })   

async def validate_code_controller(db_conn: DatabaseConnection, #Para futura implementacion de guardar RecoveryCode en DDBB
                                   validate_code_request: ValidateRecoveryCodeRequest)-> JSONResponse:
    
    code_manager = PasswordRecoveryCodeManager()
    try:
        is_valid = await concurrency.run_in_threadpool(code_manager.validate_code,
                                                       validate_code_request.code,
                                                       validate_code_request.user_email)
    except ExpiredCodeError:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= {
                "status": "error",
                "message": "El código ha expirado. Solicíte un nuevo código."
            }
        )
        
    if not is_valid:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= {
                "status": "error",
                "message": "El código es incorrecto."
            }
        )
    
    return JSONResponse(
            status_code= status.HTTP_200_OK,   
            content={
                "status": "success",
                "message": "Código validado."}
            )

async def updated_password_controller(db_conn: DatabaseConnection, new_password: str, email: str) -> JSONResponse:
    """
    Controlador para actualizar la contraseña de un usuario.
    
    Args:
        db_conn (DatabaseConnection): Conexión a la base de datos.
        new_password (str): Nueva contraseña del usuario.
        email (str): Email del usuario cuya contraseña se va a actualizar.

    Returns:
        JSONResponse: Respuesta JSON con el estado de la operación y el mensaje correspondiente.
    """
    try:
        user = await get_user_by_email(db_conn= db_conn, email= email)
        if not user:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail={
                    "status": "error",
                    "message": "El email no esta registrado en la base de datos."
                }
            )
        
        hash = hashed_password(password= new_password)
        user.password = hash  # Asignación de contraseña hasheada al usuario
        
        await update_user(db_conn= db_conn, username= user.username, updated_user= user)
        
        
        return JSONResponse(
            status_code= status.HTTP_200_OK,
            content={
                "status": "success",
                "message": "Contraseña actualizada correctamente."
            }
        )
    
    except Exception as e:
        raise HTTPException(
            status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "error",
                "message": str(e)
            }
        )
    