import bcrypt as bc

def hashed_password(password: str) -> str:
    """
    Genera un hash seguro para una contraseña utilizando bcrypt.

    Args:
        password (str): La contraseña en texto plano que se desea hashear.

    Returns:
        str: La contraseña hasheada en formato de cadena.
    """
    salt = bc.gensalt()
    hash = bc.hashpw(password=password.encode(), salt=salt)
    return hash.decode()

def validate_password(password: str, hashed_password: str) -> bool:
    """
    Valida si una contraseña en texto plano coincide con una contraseña hasheada.

    Args:
        password (str): La contraseña en texto plano que se desea validar.
        hashed_password (str): La contraseña hasheada con la que se desea comparar.

    Returns:
        bool: True si la contraseña en texto plano coincide con la contraseña hasheada, False en caso contrario.
    """
    return bc.checkpw(password=password.encode(), hashed_password=hashed_password.encode())
