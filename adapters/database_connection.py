from abc import ABC, abstractmethod

class DatabaseConnection(ABC):
    
    @abstractmethod
    async def connect(self) -> None: pass
    
    @abstractmethod
    async def execute(self, query: str, params: list) -> list[tuple]: pass
    
    @abstractmethod
    async def close(self) -> None: pass
    