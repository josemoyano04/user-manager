from abc import ABC, abstractmethod

class DatabaseConnection(ABC):
    """
    Clase abstracta que define la interfaz para las conexiones a bases de datos.

    Esta clase proporciona métodos abstractos que deben ser implementados por cualquier clase que herede de ella.
    Los métodos incluyen la conexión a la base de datos, la ejecución de consultas y el cierre de la conexión.
    """

    @abstractmethod
    async def connect(self) -> None:
        """
        Establece la conexión a la base de datos.

        Este método debe ser implementado por las subclases para definir cómo se establece la conexión.
        """
        pass
    
    @abstractmethod
    async def execute(self, query: str, params: list) -> list[tuple]:
        """
        Ejecuta una consulta en la base de datos.

        Args:
            query (str): La consulta SQL a ejecutar.
            params (list): Lista de parámetros para la consulta.

        Returns:
            list[tuple]: Resultados de la consulta.

        Este método debe ser implementado por las subclases para definir cómo se ejecutan las consultas.
        """
        pass
    
    @abstractmethod
    async def close(self) -> None:
        """
        Cierra la conexión a la base de datos.

        Este método debe ser implementado por las subclases para definir cómo se cierra la conexión.
        """
        pass
