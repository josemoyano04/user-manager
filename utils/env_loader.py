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
            
            if ENV_PATH:
                print(f"Archivo .env cargado desde: {ENV_PATH}")
                dotenv.load_dotenv(ENV_PATH)
            else:
                print("Archivo .env no encontrado. Cargando variables de entorno del sistema.")
    
            try:        
                self.__env_variables = { 
                                        key: os.getenv(key) for 
                                        key in 
                                        os.environ.keys()
                                        }
            except Exception as e:
                print(f"Error al cargar el archivo .env: {e}")
                

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