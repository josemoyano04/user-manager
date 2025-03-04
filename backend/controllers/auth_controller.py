from fastapi.responses import JSONResponse
from errors.token_format_error import TokenFormatError
from services import auth_services as at
from fastapi import HTTPException, status, Depends
from models.responses.token_response import Token
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from errors.users_errors import UserNotFoundError, UsernameNotFoundError
from jwt import InvalidTokenError, ExpiredSignatureError 

async def login_for_access_token_controller(form_data: OAuth2PasswordRequestForm) -> JSONResponse:
    """
    Controlador para el inicio de sesión y obtención de un token de acceso.

    Este controlador recibe las credenciales del usuario a través de un formulario
    OAuth2 y, si son válidas, devuelve un token de acceso en formato JSON.

    Args:
        form_data (OAuth2PasswordRequestForm): Datos del formulario que contienen
        el nombre de usuario y la contraseña.

    Returns:
        JSONResponse: Respuesta JSON que contiene el estado de la operación y el token de acceso.

    Raises:
        HTTPException: Si las credenciales de autenticación no son válidas.
    """
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        headers={
            "WWW-Authenticate": "Bearer"
        },
        detail={
            "status": "error",
            "message": "La credenciales de autenticación no son válidas."
        }
    )
    
    try:
        token = await at.login_for_access_token(form_data)

        response = JSONResponse(
            status_code=status.HTTP_200_OK,
            headers={
                "WWW-Authenticate": "Bearer"
            },
            content={
                "status": "success",
                "access_token": token.token,
                "token_type": token.token_type
            }
        )
        return response
        
    except UserNotFoundError as e:
        raise credential_exception


async def get_current_user_controller(token: str) -> JSONResponse:
    """
    Controlador para obtener la información del usuario actual a partir de un token.

    Este controlador recibe un token y devuelve la información del usuario
    asociado a ese token en formato JSON.

    Args:
        token (str): El token de acceso del usuario.

    Returns:
        JSONResponse: Respuesta JSON que contiene el estado de la operación y los datos del usuario.

    Raises:
        HTTPException: Si el usuario no se encuentra o si hay un problema con el token.
    """
    try:
        user = await at.get_current_user(token)
        
        response = JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status": "success",
                "data": user.model_dump()
            }
        )
        
        return response
    
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status": "error",
                "message": "Usuario no encontrado en base de datos."
            }
        )
    except UsernameNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "status": "error",
                "message": "'username' no encontrado en token."
            },
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )
    except TokenFormatError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "status": "error",
                "message": "Formato de token no válido."
            }
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= {
                "status" : "error",
                "message" : "Token invalido. Vuelva a iniciar sesión."
            }
        )
        
    except ExpiredSignatureError:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= {
                "status" : "error",
                "message" : "Token expirado. Vuelva a iniciar sesión."
            }
        )
    
