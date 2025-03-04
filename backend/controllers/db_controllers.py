import services.db_services as db
import services.hashing_service as hs
from models.user_db import User, UserDB
from libsql_client import LibsqlError
from fastapi.responses import JSONResponse
from fastapi import status, HTTPException
from models.request.delete_user_request import DeleteUserRequest
from models.request.update_user_request import UpdateUserRequest 
from models.request.add_user_request import AddUserRequest


#CONTROLADORES NECESARIOS

async def add_user_controller(request: AddUserRequest) -> JSONResponse:
    #Proceso de hashing de contraseña
    hash = hs.hashed_password(password= request.user.password)
    request.user.password = hash  # → Asignacion de contraseña hasheada al usaurio  
    
    #Construccion de usuarrio a devolver en JSONResponse
    response_user = User(**dict(request.user))
    
    
    #Proceso de almacenamiento en db
    try:
        client = await db.create_client()
        
        #Primera validacion de unicidad de datos
        if not await db.is_unique(client, request.user):
            raise HTTPException(
            status_code= status.HTTP_409_CONFLICT,
            detail= {
                "status": "error",
                "data": {"user": response_user.model_dump()},
                "message": "El 'email' y/o 'username' ya existen para otro usuario."
            }
        )
        
        #Proceso de almacenamiento en DDBB
        client = await db.create_client()
        await db.add_user(client, request.user)
        
        return JSONResponse(
            status_code= status.HTTP_200_OK,
            content= {
                "status": "success",
                "data": {"user": response_user.model_dump()},
                "message": "Usuario registrado correctamente."
            })
    
    #Segunda validacion de unicidad de datos en caso de error.
    except LibsqlError as error:
        raise HTTPException(
            status_code= status.HTTP_409_CONFLICT,
            detail= {
                "status": "error",
                "data": {"user": response_user.model_dump()},
                "message": "El 'email' o 'username' ya existen para otro usuario.",
                "error detail" : error
            }
        )
    finally:
        await client.close()
        
async def get_user_controller(username: str) -> JSONResponse:
    
    try:
        client = await db.create_client()
        user = await db.get_user(client, username)
        if not user:
            raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= {
                "status": "error",
                "message": f"No se encontró el usuario con 'username': {username}."
            }
        )
        
        return JSONResponse(status_code= status.HTTP_200_OK,
                            content= {"status" : "success",
                                      "data" : {"user": user.model_dump()},
                                      "message": "Usuario encontrado conn exito"})
        
    except LibsqlError as error:
        raise HTTPException(
            status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= {
                "status" : "error",
                "message" : "Ocurrio un error inesperado.",
                "error details" : {error}
            }
        )
    finally:
        await client.close()

async def delete_user_controller(request: DeleteUserRequest) -> JSONResponse: 
    
    try:
        client = await db.create_client()
        #Validacion de username existente
        exist_user = await db.exists_username(client, request.username) #El metodo cierra la conexion del cliente
        
        if not exist_user:
            raise HTTPException(
            status_code= status.HTTP_409_CONFLICT,
            detail= {
                "status": "error",
                "data": {"username": request.username},
                "message": "El 'username' no existe."
            }
        )   
            
        #Proceso de eliminacion de usuario
        client = await db.create_client() #Nuevo cliente
        await db.delete_user(client, request.username)
        return JSONResponse(
            status_code= status.HTTP_200_OK,
            content= {
                "status" : "success",
                "data" : request.username,
                "message" : f"Usuario '{request.username}' eliminado con exito."
            }
        )
    
    except LibsqlError:
        raise HTTPException(
            status_code= status.HTTP_409_CONFLICT,
            detail= {
                "status": "error",
                "data": {"username": request.username},
                "message": "El 'username' no existe."
            }
        )
    finally:
        await client.close()
        
async def update_user_controller(request: UpdateUserRequest) -> JSONResponse:
    
    client = await db.create_client()
    try:
    
        #Validacion de existencia de usuario a actualizar
        exist_user = await db.exists_username(client, request.username) #Cierra el cliente, por lo que se vuelve a iniciar uno nuevo
        
        if not exist_user:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail= {
                    "status": "error",
                    "data": {"username": request.username},
                    "message": "El 'username' no existe."
                }
            )
        
        #Validaciones de unicidad de datos del usuario actualizado
        client = await db.create_client()
        unique = await db.is_unique(client, request.updated_user, for_update_user= True)
        if not unique:
            raise HTTPException(
                status_code= status.HTTP_409_CONFLICT,
                detail= {
                    "status": "error",
                    "data": {"username": request.username},
                    "message": "El 'email' y/o 'username' ya existen para otro usuario."
                }
            )
    
    
        #Hasheo de contraseña nueva
        request.updated_user.password = hs.hashed_password(request.updated_user.password)
        
        #Proceso de actualizacion del usuario en la base de datos  
        client = await db.create_client()
        await db.update_user(
                client= client, 
                username= request.username, 
                updated_user= request.updated_user)
        
        #Retorno de JSONResponse
        return JSONResponse(
            status_code= status.HTTP_200_OK,
            content= {
                "status" : "success",
                "message" : "Usuario actualizado con exito."
            }
        )
        
    except LibsqlError as error:
        raise HTTPException(
            status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= {
                "status" : "error",
                "message" : "Ocurrio un error al intentar actualizar el usuario.",
                "error details" : {error}
            }
        )
    finally:
        await client.close()