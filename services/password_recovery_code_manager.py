from utils.env_loader import EnvManager
from models.recovery_code import RecoveryCode
from errors.recovery_code_errors import ExpiredCodeError


class PasswordRecoveryCodeManager():
    __instance = None
    
    
    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super(PasswordRecoveryCodeManager, cls).__new__(cls)
        return cls.__instance
    
    def __init__(self):
        if not hasattr(self, "_initialized"):
            self._initialized = True
            self.users_codes: dict[str, RecoveryCode] = {}
            
            self.min_code_lifetme = int(EnvManager().get("CODE_EXPIRE_MINUTES"))
        
        
    def generate_code(self, user_email: str) -> RecoveryCode:
        code = RecoveryCode(minutes_of_code_lifetime= self.min_code_lifetme)
        self.save_code(user_email= user_email, code= code)
        return code
    
    def save_code(self, user_email: str, code: RecoveryCode) -> None:
        self.users_codes[user_email] = code
        
    def validate_code(self, code: str, email: str) -> bool:
        """
        La función valida el código de recuperación de contraseña para un usuario específico.
        Si el código es válido, se elimina de la lista de códigos guardados.
        
        raises: ExpiredCodeError si el código ha expirado.
        """
        saved_code = self.users_codes.get(email)
        
        if saved_code is None:
            return False
        
        if not saved_code.is_valid(): 
            raise ExpiredCodeError("Código de recuperación de contraseña expirado.")

        
        validated = code == saved_code.code
    
        if validated:
            self.users_codes.pop(email, None)
        
        return validated