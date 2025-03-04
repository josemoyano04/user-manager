import json
import pytest
from controllers import db_controllers as c
from models.user_db import UserDB
from services import db_services as db, hashing_service as hs, db_clean_after_test as clean
from models.request.add_user_request import AddUserRequest
from models.request.update_user_request import UpdateUserRequest
from models.request.delete_user_request import DeleteUserRequest

#=======================================FIXTURES=======================================

@pytest.fixture(scope="module")
def fake_user():
    return UserDB(
        full_name= "User Test",
        username= "userTest",
        email= "userTest@example.com",
        password= "testing"
    )
@pytest.fixture(scope="module")
def updated_fake_user():
    return UserDB(
        full_name= "User Test FullName",
        username= "userTest",
        email= "userTestUp@example.com",
        password= "testingUpdate"
    )

@pytest.fixture(scope= "module")
async def create_data_in_database(fake_user):
    
    sequence_data = await clean.get_sqlite_sequence()
    #Espera para la ejecucion del test.
    yield
    
    #Limpieza de datos cargados para pruebas   
    await clean.restore_sqlite_sequence(sequence_data)
    
@pytest.fixture(scope= "module")
def add_user_request(fake_user):
    return AddUserRequest(user= fake_user)

@pytest.fixture(scope= "module")
def update_user_request(fake_user, updated_fake_user):
    return UpdateUserRequest(username= fake_user.username,
                             updated_user= updated_fake_user)

@pytest.fixture(scope= "module")
def delete_user_request(fake_user):
    return DeleteUserRequest(username= fake_user.username)
#=======================================TEST=======================================

@pytest.mark.asyncio
async def test_add_user_controller(add_user_request):
    res = await c.add_user_controller(add_user_request)
    assert res.status_code == 200
    

@pytest.mark.asyncio
async def test_update_user_controller(update_user_request):
    res = await c.update_user_controller(update_user_request)
    assert res.status_code == 200
    
@pytest.mark.asyncio
async def test_delete_user_controller(delete_user_request):
    res = await c.delete_user_controller(delete_user_request)
    assert res.status_code == 200