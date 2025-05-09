import asyncio
from adapters.database_connection import DatabaseConnection
from models.user_db import User, UserDB
from typing import Union


#TODO actualizar documentacion
# Bloqueo para controlar concurrencia de conexiones.
look = asyncio.locks.Lock()

# Operaciones CRUD

async def add_user(db_conn: DatabaseConnection, user: UserDB) -> None:
    """
    Agrega un nuevo usuario a la base de datos.

    Args:
        db_conn (DatabaseConnection): Cliente de conexión a la base de datos.
        user (UserDB): El objeto UserDB que contiene la información del usuario a agregar.
    """
    try:
        async with look:
            await db_conn.connect()
            await db_conn.execute(
                "INSERT INTO user(full_name, username, email, hashed_password) VALUES (?, ?, ?, ?);",
                [*user.model_dump().values()]
            )
    finally:
        await db_conn.close()

async def get_user(db_conn: DatabaseConnection, username: str, visible_password: bool = False) -> User | UserDB | None:
    """
    Obtiene un usuario de la base de datos a partir de su nombre de usuario.

    Args:
        db_conn (DatabaseConnection): Cliente de conexión a la base de datos.
        username (str): El nombre de usuario del usuario a buscar.
        visible_password (bool): Flag para indicar si retornar el hashed_password del usuario.
    Returns:
        User | UserDB | None: Un objeto User si se encuentra el usuario, de lo contrario None y UserDB si hidden_password es True.
    """
    try:
        async with look:
            await db_conn.connect()
            result = await db_conn.execute("""SELECT full_name, username, email, hashed_password
                                        FROM user WHERE username = ?;""", [username])
            
            row = result[0] if len(result) == 1 else None #TODO mejorar logica de recuperacion de usuario.
            
            if row:
                user_data = {"full_name": row[0], "username": row[1], "email": row[2]}
                if visible_password:
                    user_data["password"] = row[3]
                    return UserDB(**user_data)
                
                return User(**user_data)
            return None
    finally:
        await db_conn.close()

async def delete_user(db_conn: DatabaseConnection, username: str) -> None:
    """
    Elimina un usuario de la base de datos a partir de su nombre de usuario.

    Args:
        db_conn (DatabaseConnection): Cliente de conexión a la base de datos.
        username (str): Nombre de usuario del usuario a eliminar.
    """
    try:
        async with look:
            await db_conn.connect()
            await db_conn.execute("DELETE FROM user WHERE username = ?", [username])
    finally:
        await db_conn.close()

async def update_user(db_conn: DatabaseConnection, username: str, updated_user: UserDB) -> None:
    """
    Actualiza la información de un usuario en la base de datos.

    Args:
        db_conn (DatabaseConnection): Cliente de conexión a la base de datos.
        username (str): Nombre de usuario del usuario a actualizar.
        updated_user (UserDB): Objeto UserDB que contiene la nueva información del usuario.
    """
    try:
        async with look:
            await db_conn.connect()
            await db_conn.execute(
                """UPDATE user
                SET full_name = ?, username = ?, email = ?, hashed_password = ?
                WHERE username = ?""",
                [updated_user.full_name, updated_user.username, updated_user.email,
                updated_user.password, username]
            )
    finally:
        await db_conn.close()

async def exists_username(db_conn: DatabaseConnection, username: str) -> bool:
    """
    Verifica si el nombre de usuario exista en la base de datos.

    Args:
        db_conn (DatabaseConnection): Cliente de conexión a la base de datos.
        username (str): Nombre de usuario a validar.

    Returns:
        bool: Devuelve True si el nombre de usuario existe en la base de datos,
              de lo contrario, devuelve False.
    """
    try:
        async with look:
            await db_conn.connect()
            result = await db_conn.execute("SELECT * FROM user WHERE username = ?;", [username])
            
            return len(result) != 0 
    finally:
        await db_conn.close()
        
async def is_unique(db_conn: DatabaseConnection, user: User, for_update_user: bool = False) -> bool:
        """
        Verifica la existencia de un usuario en la base de datos basado en el nombre de usuario y el correo electrónico.

        Args:
            db_conn (DatabaseConnection): Cliente de conexión a la base de datos.
            user (User): Un objeto que contiene el nombre de usuario y el correo electrónico a verificar.
            for_update_user (bool): Un indicador que determina si se está verificando para actualizar un usuario 
                existente. Si se indica como 'True', se ajusta la consulta para aceptar al menos una fila, la cual
                es resultante del usuario existente a actualizar.

        Returns:
            bool: Devuelve True si el nombre de usuario y el correo electrónico son únicos (no existen en la base de datos)
                cuando `for_update_user` es False, o si existe exactamente un usuario cuando `for_update_user` es True.
                Devuelve False en caso contrario.
        """
        try:
            async with look:
                await db_conn.connect()
                result = await db_conn.execute("SELECT * FROM user WHERE username = ? OR email = ?;", 
                                            [user.username, user.email])
                
                return len(result) == 0 if not for_update_user else len(result) == 1
        finally:
            await db_conn.close()

async def get_user_by_email(db_conn: DatabaseConnection, email: str, 
                            visible_password: bool = False) -> Union[UserDB, User, None]:
    """
    Obtiene un usuario de la base de datos a partir de su correo electrónico.

    Args:
        db_conn (DatabaseConnection): Cliente de conexión a la base de datos.
        email (str): El correo electrónico del usuario a buscar.

    Returns:
        UserDB | None: Un objeto UserDB si se encuentra el usuario, de lo contrario None.
    """
    try:
        async with look:
            await db_conn.connect()
            result = await db_conn.execute(""" SELECT full_name, username, email, hashed_password
                                               FROM user WHERE email = ?;""", [email])
            
            row = result[0] if len(result) == 1 else None
            if row:
                user_data = {"full_name": row[0], "username": row[1], "email": row[2]}
                if visible_password:
                    user_data["password"] = row[3]
                    
                    return UserDB(**user_data)
                return User(**user_data)
            return None
    finally:
        await db_conn.close()
        