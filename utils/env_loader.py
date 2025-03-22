import os
import dotenv

#TODO documentar
class EnvManager:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        if not hasattr(self, "__initialized"):
            self.__initialized = True
            
            ENV_PATH = dotenv.find_dotenv(".env")  
            if not ENV_PATH:
                raise FileNotFoundError(f"No se encontró el archivo .env en la ruta especificada.")
            
            dotenv.load_dotenv(ENV_PATH) 
            
            self.__env_variables = { 
                                    key: value for 
                                    key, value in 
                                    os.environ.items() 
                                    if key in dotenv.dotenv_values(ENV_PATH)
                                  }


    def get(self, key: str, default=None):
        """Obtiene una variable de entorno con una clave específica."""
        return self.__env_variables.get(key, default)

    def get_all(self):
        """Devuelve todas las variables de entorno como un diccionario."""
        return self.__env_variables


# Ejemplo de uso
if __name__ == "__main__":
    env = EnvManager()
    print(env.get_all())