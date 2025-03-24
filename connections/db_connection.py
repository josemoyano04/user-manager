from utils.env_loader import EnvManager
from adapters.adapter_db_conn_libsql import AdapterDBConnLibsqlClient

def db_conn_libsql_client() -> AdapterDBConnLibsqlClient:
    """
    Retorna una conexión a una base de datos, obteniendo los datos de conexión a 
    partir de las variables de entorno correspondientes.

    Returns:
        AdapterDBConnLibsqlClient: Instancia de la clase que implementa el patrón adaptador 
        para la conexión a la base de datos.
    """
    ENV = EnvManager()

    DATABASE_URL = ENV.get("PRODUCTION_DATABASE_URL")
    DATABASE_AUTH_TOKEN = ENV.get("PRODUCTION_DATABASE_AUTH_TOKEN")

    DB_CONN = AdapterDBConnLibsqlClient(database_url=DATABASE_URL, 
                                        auth_token=DATABASE_AUTH_TOKEN)

    return DB_CONN
