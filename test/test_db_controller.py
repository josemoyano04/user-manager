import json
from fastapi import HTTPException
import pytest
from models.user import User
from controllers import db_controllers as controller
from models.request import add_user_request, update_user_request
from services.auth_services import create_access_token
from services.db_services import get_user
#==================== FIXTURES ====================
from test.common_fixtures import database_mock, user_fixture, updated_user_fixture

@pytest.fixture(scope= 'module')
def add_user_request_fixture(user_fixture):
    return add_user_request.AddUserRequest(user= user_fixture)

@pytest.fixture(scope= 'module')
def updated_user_request_fixture(user_fixture, updated_user_fixture):
    return update_user_request.UpdateUserRequest(username= user_fixture.username,
                                                 updated_user= updated_user_fixture)

@pytest.fixture(scope= "module")
async def access_token_fixture(user_fixture):
    return create_access_token(username= user_fixture.username)

#====================== TEST ======================
async def test_add_user_controller(database_mock, add_user_request_fixture):
    response = await controller.add_user_controller(db_conn= database_mock, 
                                                    request= add_user_request_fixture)
    
    decode_content = response.body.decode(encoding= "utf-8")
    content = json.loads(decode_content)
    
    assert response.status_code == 200
    assert content["status"] == "success"
    
    #Intento de volver a agregar un usuario con datos repetidos
    with pytest.raises(HTTPException) as error:
        response = await controller.add_user_controller(db_conn= database_mock,
                                                        request= add_user_request_fixture)
    assert error.value.status_code == 409 # CONFLICT

async def test_get_user_controller(database_mock, user_fixture):
    response = await controller.get_user_controller(db_conn= database_mock,
                                                    username= user_fixture.username)
    
    content = json.loads(response.body.decode(encoding= "utf-8"))
    
    assert response.status_code == 200
    assert content["status"] == "success"
    
    user = User(**content["data"])
    
    assert user.full_name == user_fixture.full_name
    assert user.username == user_fixture.username
    assert user.email == user_fixture.email
    
    with pytest.raises(HTTPException) as error:
        response = await controller.get_user_controller(db_conn= database_mock,
                                                  username= "nonexistent_username")

    assert error.value.status_code == 404 # NOT FOUND

async def test_update_user_controller(database_mock, access_token_fixture, updated_user_request_fixture):

    response = await controller.update_user_controller(db_conn= database_mock,
                                                       request= updated_user_request_fixture,
                                                       token= access_token_fixture)
    assert response.status_code == 200

    with pytest.raises(HTTPException) as error:
        response = await controller.update_user_controller(db_conn= database_mock,
                                                     request= updated_user_request_fixture,
                                                     token= "fake_token")

    assert error.value.status_code == 401 # UNAUTHORIZED    
    
async def test_delete_user_controller(database_mock, access_token_fixture, user_fixture):
    
    with pytest.raises(HTTPException) as error:
        response = await controller.delete_user_controller(db_conn= database_mock,
                                                     token= "fake_token")

    assert error.value.status_code == 401 # UNAUTHORIZED    
    
    response = await controller.delete_user_controller(db_conn= database_mock,
                                                       token= access_token_fixture)
    assert response.status_code == 200
    
    user = await get_user(db_conn= database_mock,
                          username= user_fixture.username)
    assert user is None
    
    