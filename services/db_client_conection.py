#TODO Pendiente de integración.

import os
import libsql_client as lb
from dotenv import load_dotenv, find_dotenv

#Carga de variables de entorno
ENV_PATH = find_dotenv("../.env")
load_dotenv(ENV_PATH)

#Datos de conexion a DDBB
DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_AUTH_TOKEN = os.getenv("DATABASE_AUTH_TOKEN")


#==================== Service ====================
async def create_client():
    """
    Crea un cliente de conexión a la base de datos utilizando la biblioteca libsql_client.
    El metodo hace uso de la URL y AUTH_TOKEN alojado en las variables de entorno.

    Returns:
        lb.Client: Un objeto cliente que permite interactuar con la base de datos.

    Raises:
        LibsqlError: Si hay un error al crear el cliente respecto a la url o token de autenticacion.

    """
    return lb.create_client(url= DATABASE_URL,
                          auth_token= DATABASE_AUTH_TOKEN)
