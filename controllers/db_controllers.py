from adapters.database_connection import DatabaseConnection
from models.user_db import User
import services.db_services as db
import services.hashing_service as hs
from libsql_client import LibsqlError
from fastapi import status, HTTPException
from fastapi.responses import JSONResponse
from models.request.add_user_request import AddUserRequest
from models.request.update_user_request import UpdateUserRequest 
from services.auth_services import validate_access_token, get_username_from_token

#======================================== CONTROLLERS ================================================#

async def add_user_controller(db_conn: DatabaseConnection, request: AddUserRequest) -> JSONResponse:
    """
    Controlador para agregar un nuevo usuario.

    Args:
        db_conn (DatabaseConnection): Conexión a la base de datos.
        request (AddUserRequest): Solicitud que contiene los datos del nuevo usuario.

    Returns:
        JSONResponse: Respuesta JSON con el estado de la operación y los datos del usuario registrado.
    """
    # Proceso de hashing de contraseña
    hash = hs.hashed_password(password=request.user.password)
    request.user.password = hash  # Asignación de contraseña hasheada al usuario  

    # Construcción de usuario a devolver en JSONResponse
    response_user = User(**dict(request.user))

    # Proceso de almacenamiento en db
    try:        
        # Primera validación de unicidad de datos
        if not await db.is_unique(db_conn=db_conn, user=request.user):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "status": "error",
                    "data": {"user": response_user.model_dump()},
                    "message": "El 'email' y/o 'username' ya existen para otro usuario."
                }
            )
        
        # Proceso de almacenamiento en DDBB
        await db.add_user(db_conn=db_conn, user=request.user)
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status": "success",
                "data": {"user": response_user.model_dump()},
                "message": "Usuario registrado correctamente."
            }
        )

    # Segunda validación de unicidad de datos en caso de error.
    except LibsqlError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "status": "error",
                "data": {"user": response_user.model_dump()},
                "message": "El 'email' o 'username' ya existen para otro usuario.",
                "error detail": error
            }
        )

async def get_user_controller(db_conn: DatabaseConnection, username: str) -> JSONResponse:
    """
    Controlador para obtener un usuario por su nombre de usuario.

    Args:
        db_conn (DatabaseConnection): Conexión a la base de datos.
        username (str): Nombre de usuario del usuario a buscar.

    Returns:
        JSONResponse: Respuesta JSON con el estado de la operación y los datos del usuario encontrado.
    """
    try:
        user = await db.get_user(db_conn=db_conn, username=username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "status": "error",
                    "message": f"No se encontró el usuario con 'username': {username}."
                }
            )
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status": "success",
                "message": "Usuario encontrado con éxito",
                "data": user.model_dump()
            }
        )
        
    except LibsqlError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "error",
                "message": "Ocurrió un error inesperado.",
                "error details": {error}
            }
        )

async def update_user_controller(db_conn: DatabaseConnection, request: UpdateUserRequest, token: str) -> JSONResponse:
    """
    Controlador para actualizar los datos de un usuario.

    Args:
        db_conn (DatabaseConnection): Conexión a la base de datos.
        request (UpdateUserRequest): Solicitud que contiene los datos del usuario a actualizar.
        token (str): Token de acceso del usuario.

    Returns:
        JSONResponse: Respuesta JSON con el estado de la operación.
    """
    if not await validate_access_token(db_conn=db_conn, token=token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "status": "error",
                "message": "Usuario no autenticado."
            }
        )

    try:    
        # Validaciones de unicidad de datos del usuario actualizado
        unique = await db.is_unique(db_conn=db_conn, user=request.updated_user, for_update_user=True)
        if not unique:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "status": "error",
                    "data": {"username": request.username},
                    "message": "Datos no actualizados. El 'email' y/o 'username' ya existen para otro usuario."
                }
            )

        # Hasheo de contraseña nueva
        request.updated_user.password = hs.hashed_password(request.updated_user.password)
        
        # Proceso de actualización del usuario en la base de datos  
        await db.update_user(
            db_conn=db_conn, 
            username=request.username, 
            updated_user=request.updated_user
        )
        
        # Retorno de JSONResponse
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status": "success",
                "message": "Usuario actualizado con éxito."
            }
        )
        
    except LibsqlError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "error",
                "message": "Ocurrió un error al intentar actualizar el usuario.",
                "error details": {error}
            }
        )

async def delete_user_controller(db_conn: DatabaseConnection, token: str) -> JSONResponse: 
    """
    Controlador para eliminar un usuario.

    Args:
        db_conn (DatabaseConnection): Conexión a la base de datos.
        token (str): Token de acceso del usuario.

    Returns:
        JSONResponse: Respuesta JSON con el estado de la operación.
    """
    # Validaciones de token
    if not await validate_access_token(db_conn=db_conn, token=token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "status": "error",
                "message": "Usuario no autenticado."
            }
        )
    
    # Obtención de username guardado en el token
    username = get_username_from_token(token)
    
    try:
        # Proceso de eliminación de usuario 
        await db.delete_user(db_conn=db_conn, username=username)
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status": "success",
                "data": username,
                "message": f"Usuario '{username}' eliminado con éxito."
            }
        )
    
    except LibsqlError as e:
        msg = ["no existe", "not exists"]
        if any(message in str(e) for message in msg):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "status": "error",
                    "data": {"username": username},
                    "message": f"Error. El username '{username}' no existe en la base de datos."
                }
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "status": "error",
                    "data": {"username": username},
                    "message": f"Error interno del servidor."
                }
            )
