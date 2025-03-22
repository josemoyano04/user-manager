import sqlite3
from adapters.database_connection import DatabaseConnection
from errors.database_errors import DatabaseConnectionError, DatabaseQueryError


class AdapterDBConnMemorySqlite3Test(DatabaseConnection):
    """
    Clase adaptadora para gestionar la conexión a una base de datos SQLite en memoria.

    Esta clase implementa el patrón Singleton para asegurar que solo haya una instancia de la conexión a la base de datos.
    Hereda de la clase `DatabaseConnection`.

    Attributes:
        __connection (sqlite3.Connection | None): Conexión a la base de datos SQLite en memoria.
    """
    
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    
    def __init__(self):
        """
        Inicializa una nueva instancia de AdapterDBConnMemorySqlite3Test.
        """
        if not hasattr(self, "__initialized"):
            self.__initialized = True
            self.__connection: sqlite3.Connection | None = None
            
    async def connect(self) -> None:
        """
        Establece la conexión a la base de datos en memoria y crea la tabla de usuarios.

        Raises:
            DatabaseConnectionError: Si ocurre un error al intentar conectar a la base de datos.
        """
        if self.__connection is None:
            self.__connection = sqlite3.connect(":memory:")
            cursor = self.__connection.cursor()
            cursor.execute("""
                CREATE TABLE user (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name TEXT NOT NULL,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    hashed_password TEXT NOT NULL
                )
            """)
    
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
        if self.__connection is None:
            raise DatabaseConnectionError("La conexión a la base de datos está cerrada.")
        
        try:
            cursor = self.__connection.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
            return results
        
        except Exception as E:
            raise DatabaseQueryError(f"Error al ejecutar la consulta. Detalles: {str(E)}")

    async def close(self) -> None:
        """
        Cierra la conexión a la base de datos.
        """
        if self.__connection is None:
            return
        self.__connection.close()
