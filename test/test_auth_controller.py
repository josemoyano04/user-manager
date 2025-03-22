import json
import pytest
from models.user_db import UserDB
from fastapi import HTTPException
from errors.testing_errors import FixtureError
from models.responses.token_response import Token
from controllers import auth_controller as controller
from fastapi.security import OAuth2PasswordRequestForm
from services import hashing_service as hs, db_services as db

#==================== FIXTURES ====================
from test.common_fixtures import database_mock, user_fixture

@pytest.fixture(scope= "module")
async def create_data_in_database(user_fixture, database_mock):
    
    #Creacion de datos para test en base de datos
    original_password = user_fixture.password
    hashed_password =  hs.hashed_password(user_fixture.password)
    user_fixture.password = hashed_password
    await db.add_user(db_conn= database_mock, 
                      user= user_fixture)
    
    #Restauracion de password sin hashear
    user_fixture.password = original_password
    
    #Verificacion de creacion de datos
    data = await db.get_user(db_conn= database_mock,
                       username= user_fixture.username)
    if data is None:
        raise FixtureError("Error al intentar inicializar el fixture.")

@pytest.fixture(scope= "module")
def recovered_token():
    return Token(token= "", token_type= "Bearer")
    
#==================== TEST ====================
async def test_login_for_access_token_controller(create_data_in_database, database_mock, user_fixture, recovered_token) : 

    form_data = OAuth2PasswordRequestForm(username= user_fixture.username,
                                          password= user_fixture.password)
    
    response = await controller.login_for_access_token_controller(db_conn= database_mock,
                                                                  form_data= form_data)    

    decode_content = response.body.decode("utf-8")
    content = json.loads(decode_content)
    
    assert response.status_code == 200 
    assert content["status"] == "success"
    assert "access_token" in content
    
    recovered_token.token = content["access_token"]
    
    with pytest.raises(HTTPException) as error:
        form_data.password = "Fake password"
        response = await controller.login_for_access_token_controller(db_conn= database_mock,
                                                                      form_data= form_data)
    
    assert error.value.status_code == 401 # UNAUTHORIZED
    
async def test_get_current_user_controller(database_mock, user_fixture, recovered_token):
    response = await controller.get_current_user_controller(db_conn= database_mock, 
                                                            token= recovered_token.token)

    decode_content = response.body.decode("utf-8")
    content = json.loads(decode_content)
    
    assert response.status_code == 200 
    assert content["status"] == "success"
    
    user = UserDB(**content["data"])
    
    assert user.full_name == user_fixture.full_name
    assert user.username == user_fixture.username
    assert user.email == user_fixture.email
    
    # ERROR POR INVALIDTOKEN
    with pytest.raises(HTTPException) as error:
        response = await controller.get_current_user_controller(db_conn= database_mock,
                                                                token= "Fake_token")
    
    assert error.value.status_code == 400 # BAD REQUEST