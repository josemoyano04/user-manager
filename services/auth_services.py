import os
import jwt
from models.user_db import UserDB
from dotenv import load_dotenv, find_dotenv
from errors.users_errors import UserNotFoundError
from models.responses.token_response import Token
from errors.users_errors import UserNotFoundError, UsernameNotFoundError
from errors.token_format_error import TokenFormatError
from services import db_services as db, hashing_service as hs
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Union

#========================================CONSTANTS================================================#
#Carga de varibales de entorno.
DOTENV_URL = find_dotenv("../.env")
load_dotenv(DOTENV_URL)
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES"))
print(SECRET_KEY)
print(ALGORITHM)
print(ACCESS_TOKEN_EXPIRE_MINUTES)
TOKEN_TYPE = "Bearer" 

#Constantes de servicio de base de datos.
DB_CLIENT = db.create_client

#Schema
oauth2_schema = OAuth2PasswordBearer(tokenUrl= "/login")

#========================================SERVICES================================================#
async def authenticate_user(username: str, password: str) -> bool:
    """
    Verifica las credenciales del usuario.

    Esta función busca un usuario en la base de datos utilizando el nombre de usuario proporcionado
    y valida la contraseña proporcionada contra la contraseña almacenada.

    Args:
        username (str): El nombre de usuario del usuario a autenticar.
        password (str): La contraseña del usuario a autenticar.

    Raises:
        UserNotFoundError: Si no se encuentra un usuario con el nombre de usuario proporcionado.

    Returns:
        bool: Devuelve True si las credenciales son válidas, de lo contrario, devuelve False.
    """
    db_client = await DB_CLIENT()
    user: UserDB = await db.get_user(db_client, username, hidden_password=True)
    
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
        username (str): El nombre de usuario para el cual se generará el token.

    Returns:
        str: El token de acceso JWT codificado.
    """
    # Data
    payload = {
        "sub": username,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    # Creación de JWT    
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_username_from_token(token: str) -> Union[str, None]:
    """
    Extrae el nombre de usuario de un token JWT.

    Esta función decodifica el token JWT y devuelve el nombre de usuario contenido en el payload.

    Args:
        token (str): El token JWT del cual se extraerá el nombre de usuario.

    Returns: 
        str | None: El nombre de usuario si se encuentra, de lo contrario None.
    """
    try:
        payload: dict = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username = payload.get("sub", None)
        return username if username else None
    except Exception as e:
        return None
        
async def validate_access_token(token: str) -> bool:
    """
    Valida un token de acceso JWT.

    Esta función decodifica el token y verifica si el nombre de usuario asociado existe en la base de datos.
    Tambien verifíca que el token no este expirado, y la firma del mismo.

    Args:
        token (str): El token JWT a validar.

    Returns:
        bool: Devuelve True si el token es válido y el usuario existe, de lo contrario False.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        username = get_username_from_token(token)

        if username:
            client = await DB_CLIENT()
            return await db.exists_username(client, username)
        
    except (jwt.PyJWTError):
        return False
    except KeyError:
        return False

async def get_current_user(token: str) -> UserDB: 
    """
    Recupera el usuario actual a partir de un token JWT.

    Esta función decodifica el token JWT proporcionado y busca el usuario correspondiente en la base de datos.

    Args:
        token (str): El token JWT del cual se extraerá el nombre de usuario.

    Raises:
        UserNotFoundError: Si no se encuentra un usuario con el nombre de usuario extraído del token.
        UsernameNotFoundError: Si no se encuentra el nombre de usuario en el token.
        TokenFormatError: Si el formato del token no es válido.
        InvalidTokenError: Si el token está expirado. Pertenece al módulo jwt.

    Returns:
        UserDB: El objeto de usuario correspondiente al nombre de usuario extraído del token.
    """
    db_client = await DB_CLIENT()
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username = payload["sub"]
        
        # Recuperación de username
        if not username:
            raise UsernameNotFoundError("Username no encontrado.")
        
        # Recuperación de usuario en base de datos.
        user = await db.get_user(db_client, username, hidden_password=True)
        
        if not user:
            raise UserNotFoundError("Usuario no encontrado.")
        
        return user
        
    except KeyError as e:  # A modo de prevención de formato correcto del json web token.
        raise TokenFormatError("No se encontró la clave username en el JWT decodificado")

    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError
    except jwt.InvalidTokenError:
        raise jwt.InvalidTokenError
        
async def login_for_access_token(form_data: OAuth2PasswordRequestForm) -> Token:
    """
    Maneja el proceso de inicio de sesión y devuelve un token de acceso.

    Esta función autentica al usuario utilizando las credenciales proporcionadas en el formulario
    y genera un token de acceso si las credenciales son válidas.

    Args:
        form_data (OAuth2PasswordRequestForm): El formulario que contiene el nombre de usuario y la contraseña.

    Raises:
        UserNotFoundError: Si no se encuentra un usuario con el nombre de usuario proporcionado.

    Returns:
        Token: Un objeto que contiene el token de acceso y el tipo de token.
    """
    user = await authenticate_user(username=form_data.username,
                                   password=form_data.password)
    
    if not user:
        raise UserNotFoundError(f"No se encontró el usuario con username: {form_data.username}")

    access_token = create_access_token(username=form_data.username)
    
    return Token(token=access_token, token_type=TOKEN_TYPE)
