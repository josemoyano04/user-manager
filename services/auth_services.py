import jwt
from models.user_db import UserDB
from utils.env_loader import EnvManager
from errors.users_errors import UserNotFoundError
from models.responses.token_response import Token
from datetime import datetime, timedelta, timezone
from errors.token_format_error import TokenFormatError
from adapters.database_connection import DatabaseConnection
from services import db_services as db, hashing_service as hs
from errors.users_errors import UserNotFoundError, UsernameNotFoundError
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

#========================================CONSTANTS================================================#
ENV = EnvManager()

SECRET_KEY = ENV.get("JWT_SECRET_KEY")
ALGORITHM = ENV.get("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(ENV.get("JWT_EXPIRE_MINUTES"))

TOKEN_TYPE = "Bearer" 


#Schema
oauth2_schema = OAuth2PasswordBearer(tokenUrl= "/")


#========================================SERVICES================================================#
async def authenticate_user(db_conn: DatabaseConnection, username: str, password: str) -> bool:
    """
    Verifica las credenciales del usuario.

    Esta función busca un usuario en la base de datos utilizando el nombre de usuario proporcionado
    y valida la contraseña proporcionada contra la contraseña almacenada.

    Args:
        db_conn (DatabaseConnection): Cliente de conexión a la base de datos.
        username (str): Nombre de usuario del usuario a autenticar.
        password (str): Contraseña del usuario a autenticar.

    Raises:
        UserNotFoundError: Si no se encuentra un usuario con el nombre de usuario proporcionado.

    Returns:
        bool: Devuelve True si las credenciales son válidas, de lo contrario, devuelve False.
    """

    user: UserDB = await db.get_user(db_conn= db_conn, 
                                     username= username, 
                                     visible_password= True)
    
    if not user:
        raise UserNotFoundError("Usuario no encontrado.")
    
    validated = hs.validate_password(password=password,
                                     hashed_password=user.password)
    
    return validated

def create_access_token(username: str) -> str:
    """
    Crea un token de acceso JWT para un usuario.

    Esta función genera un token JWT que contiene el nombre de usuario y la fecha de expiración.

    Args:
        username (str): Nombre de usuario para el cual se generará el token.

    Returns:
        str: Token de acceso JWT codificado.
    """
    # Data
    payload = {
        "sub": username,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    # Creación de JWT    
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_username_from_token(token: str) -> str | None:
    """
    Extrae el nombre de usuario de un token JWT.

    Esta función decodifica el token JWT y devuelve el nombre de usuario contenido en el payload.

    Args:
        token (str): Token JWT del cual se extraerá el nombre de usuario.

    Returns: 
        str | None: Nombre de usuario si se encuentra, de lo contrario None.
    """
    try:
        payload: dict = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username = payload.get("sub", None)
        return username if username else None
    except Exception as e:
        return None
        
async def validate_access_token(db_conn: DatabaseConnection, token: str) -> bool:
    """
    Valida un token de acceso JWT.

    Esta función decodifica el token y verifica si el nombre de usuario asociado existe en la base de datos.
    Tambien verifíca que el token no este expirado, y la firma del mismo.

    Args:
        db_conn (DatabaseConnection): Cliente de conexión a la base de datos.
        token (str): Token JWT a validar.

    Returns:
        bool: Devuelve True si el token es válido y el usuario existe, de lo contrario False.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        username = get_username_from_token(token)

        if username:
            return await db.exists_username(db_conn= db_conn, username= username)
        
    except (jwt.PyJWTError):
        return False
    except KeyError:
        return False

async def get_current_user(db_conn: DatabaseConnection, token: str) -> UserDB: 
    """
    Recupera el usuario actual a partir de un token JWT.

    Esta función decodifica el token JWT proporcionado y busca el usuario correspondiente en la base de datos.

    Args:
        db_conn (DatabaseConnection): Cliente de conexión a la base de datos.
        token (str): Token JWT del cual se extraerá el nombre de usuario.

    Raises:
        UserNotFoundError: Si no se encuentra un usuario con el nombre de usuario extraído del token.
        UsernameNotFoundError: Si no se encuentra el nombre de usuario en el token.
        TokenFormatError: Si el formato del token no es válido.
        InvalidTokenError: Si el token está expirado. Pertenece al módulo jwt.

    Returns:
        UserDB: Objeto de usuario correspondiente al nombre de usuario extraído del token.
    """
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username = payload["sub"]
        
        # Recuperación de username
        if not username:
            raise UsernameNotFoundError(f"Username no encontrado en el token.")
        
        # Recuperación de usuario en base de datos.
        user = await db.get_user(db_conn= db_conn,
                                 username= username, 
                                 visible_password= True)
        
        if not user:
            raise UserNotFoundError("Usuario no encontrado.")
        
        return user
        
    except KeyError as e:  # A modo de prevención de formato correcto del json web token.
        raise TokenFormatError("No se encontró la clave username en el JWT decodificado")

    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError
    except jwt.InvalidTokenError:
        raise jwt.InvalidTokenError
        
async def login_for_access_token(db_conn: DatabaseConnection, form_data: OAuth2PasswordRequestForm) -> Token:
    """
    Maneja el proceso de inicio de sesión y devuelve un token de acceso.

    Esta función autentica al usuario utilizando las credenciales proporcionadas en el formulario
    y genera un token de acceso si las credenciales son válidas.

    Args:
        db_conn (DatabaseConnection): Cliente de conexión a la base de datos.
        form_data (OAuth2PasswordRequestForm): El formulario que contiene el nombre de usuario y la contraseña.

    Raises:
        UserNotFoundError: Si no se encuentra un usuario con el nombre de usuario proporcionado.

    Returns:
        Token: Objeto que contiene el token de acceso y el tipo de token.
    """
    
    
    try:
        authenticated_user = await authenticate_user(db_conn= db_conn,
                                   username=form_data.username,
                                   password=form_data.password)
    
    except UsernameNotFoundError as e:
        raise UsernameNotFoundError(str(e))
    
    
    if not authenticated_user:
        raise UserNotFoundError(f"No se autenticó el usuario con username:'{form_data.username}'")

    access_token = create_access_token(username=form_data.username)
    
    return Token(token=access_token, token_type=TOKEN_TYPE)
