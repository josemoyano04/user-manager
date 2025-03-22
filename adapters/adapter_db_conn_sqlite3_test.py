import sqlite3
from adapters.database_connection import DatabaseConnection
from errors.database_errors import DatabaseConnectionError, DatabaseQueryError


class AdapterDBConnMemorySqlite3Test(DatabaseConnection):
    __instance = None
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    
    def __init__(self):
        if not hasattr(self, "__initialized"):
            self.__initialized = True
            self.__connection: sqlite3.Connection | None = None
            
    async def connect(self) -> None:
        if self.__connection is None:
            self.__connection = sqlite3.connect(":memory:")
            cursor = self.__connection.cursor()
            cursor.execute( """
                            CREATE TABLE user (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                full_name TEXT NOT NULL,
                                username TEXT UNIQUE NOT NULL,
                                email TEXT UNIQUE NOT NULL,
                                hashed_password TEXT NOT NULL
                                )
                            """
                        )
    
    async def execute(self, query: str, params: list) -> list[tuple]:
        if self.__connection is None:
            raise DatabaseConnectionError("La conexion a la base de datos esta cerrada")
        
        try:
            cursor = self.__connection.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
            return results
        
        except Exception as E:
            raise DatabaseQueryError(f"Error al ejecutar la consulta. Detalles: {str(E)}")

    async def close(self) -> None:
        if self.__connection is None:
            return
        self.__connection.close()
