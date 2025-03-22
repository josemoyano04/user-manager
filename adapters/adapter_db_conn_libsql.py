from adapters.database_connection import DatabaseConnection
import libsql_client as lb
from libsql_client import Client
from errors.database_errors import DatabaseConnectionError, DatabaseQueryError

class AdapterDBConnLibsqlClient(DatabaseConnection):
    """
    Clase adaptadora para gestionar la conexión a una base de datos utilizando el cliente Libsql.

    Esta clase implementa el patrón Singleton para asegurar que solo haya una instancia de la conexión a la base de datos.
    Hereda de la clase `DatabaseConnection`.

    Attributes:
        database_url (str): URL de la base de datos.
        auth_token (str | None): Token de autenticación para la conexión a la base de datos.
        tls (bool | None): Indica si se debe usar TLS para la conexión.
        current_client (Client | None): Cliente actual de la base de datos.
    """
    
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    
    def __init__(self, database_url: str, auth_token: str | None = None, tls: bool | None = None):
        """
        Inicializa una nueva instancia de AdapterDBConnLibsqlClient.

        Args:
            database_url (str): URL de la base de datos.
            auth_token (str | None): Token de autenticación para la conexión a la base de datos.
            tls (bool | None): Indica si se debe usar TLS para la conexión.
        """
        if not hasattr(self, "__initialized"):
            self.__initialized = True
            self.database_url = database_url
            self.auth_token = auth_token
            self.tls = tls
            self.current_client: Client = None
            
    async def connect(self) -> None:
        """
        Establece la conexión a la base de datos.

        Raises:
            DatabaseConnectionError: Si ocurre un error al intentar conectar a la base de datos.
        """
        if self.current_client is None:
            try:
                self.current_client = await lb.create_client(url=self.database_url,
                                                            auth_token=self.auth_token,
                                                            tls=self.tls)
            except Exception as error:
                raise DatabaseConnectionError(f"Error al realizar la conexión a la base de datos. Detalles: {str(error)}")
        
    async def execute(self, query: str, params: list) -> list[tuple]:
        """
        Ejecuta una consulta en la base de datos.

        Args:
            query (str): La consulta SQL a ejecutar.
            params (list): Lista de parámetros para la consulta.

        Returns:
            list[tuple]: Resultados de la consulta.

        Raises:
            DatabaseConnectionError: Si la conexión a la base de datos está cerrada.
            DatabaseQueryError: Si ocurre un error al ejecutar la consulta.
        """
        if self.current_client is None:
            raise DatabaseConnectionError("La conexión a la base de datos está cerrada.")
        
        try:
            result = await self.current_client.execute(stmt=query, args=params)
            return result.rows
        except lb.LibsqlError as error:
            raise DatabaseQueryError(f"Error al realizar la consulta. Detalles: {str(error)}")
        
    async def close(self) -> None:
        """
        Cierra la conexión a la base de datos.
        """
        if self.current_client is not None:
            await self.current_client.close()
            self.current_client = None
