import pytest
from models.user_db import UserDB
from adapters.adapter_db_conn_sqlite3_test import AdapterDBConnMemorySqlite3Test
from services.hashing_service import hashed_password

#==================== FIXTURES ====================
@pytest.fixture(scope= 'module')
async def database_mock():
    conn = AdapterDBConnMemorySqlite3Test()
    await conn.connect()
    
    original_connect = conn.connect
    original_close = conn.close
    
    async def mock_connect(): pass
    async def mock_close(): pass
    
    conn.connect = mock_connect
    conn.close = mock_close
    
    yield conn
    
    conn.connect = original_connect
    conn.close = original_close
    
    await conn.close()

@pytest.fixture(scope='module')
def user_fixture() -> UserDB:
    return UserDB(
        full_name= "test full name",
        username= "test", 
        email= "test@example.com",
        password= "test"
    )

@pytest.fixture(scope='module')
def user_with_hashed_password_fixture() -> UserDB:
    password_hashed = hashed_password("test")
    return UserDB(
        full_name= "test full name",
        username= "test", 
        email= "test@example.com",
        password= password_hashed
    )

        
    
@pytest.fixture(scope="module")
def updated_user_fixture() -> UserDB:
    return UserDB(
        full_name= "updated test full name",
        username= "test", 
        email= "updatedEmailTest@example.com",
        password= "test"
    )