from fastapi import HTTPException
import controllers.auth_controller as c

import json
import pytest
import services.db_services as db 
import services.auth_services as at
import services.hashing_service as hs 
from models.user_db import UserDB
from fastapi.security import OAuth2PasswordRequestForm

#=======================================FIXTURES=======================================
@pytest.fixture(scope="module")
def fake_user():
    return UserDB(
        full_name= "User Test",
        username= "userTest",
        email= "userTest@example.com",
        password= "testing"
    )

@pytest.fixture(scope= "module")
async def create_data_in_database(fake_user):
    
    #Creacion de datos para test en base de datos
    client = await db.create_client()
    hashed_password =  hs.hashed_password(fake_user.password)
    fake_user.password = hashed_password 
    await db.add_user(client, fake_user)
    await client.close()
    #Espera para la ejecucion del test.
    yield
    
    #Limpieza de datos cargados para pruebas   
    client = await db.create_client()
    await db.delete_user(client, fake_user.username)
    await client.close()
    
@pytest.fixture(scope= "module")
def Oauth2Form():
    return OAuth2PasswordRequestForm(username= "userTest", password= "testing")

@pytest.fixture(scope="module")
def UserNotFoundOauth2Form():
    return OAuth2PasswordRequestForm(username="User Not Found", password= "fakepass")

@pytest.fixture(scope= "module")
async def access_token(Oauth2Form):
    response = await c.login_for_access_token_controller(Oauth2Form)
    decode = response.body.decode("utf-8")
    content = json.loads(decode)
    
    return content["access_token"]

#=======================================TEST=======================================
@pytest.mark.asyncio
async def test_login_controller_success(create_data_in_database, Oauth2Form):
    
    response = await c.login_for_access_token_controller(Oauth2Form)
    decode_content = response.body.decode("utf-8")
    content = json.loads(decode_content)
    
    assert response.status_code == 200 
    assert content["status"] == "success"
    assert "access_token" in content
    assert "access_token" in content
    

@pytest.mark.asyncio
async def test_login_controller_errors(UserNotFoundOauth2Form):
    
    with pytest.raises(HTTPException) as error:
        response = await c.login_for_access_token_controller(UserNotFoundOauth2Form)
    
    assert error.value.status_code == 401 #UNAUTHORIZED
    assert error.value.detail["status"] == "error"
    assert "message" in error.value.detail 
    assert error.value.headers["WWW-Authenticate"] == "Bearer"
 
@pytest.mark.asyncio
async def test_get_current_user_success(access_token, fake_user):
    response = await c.get_current_user_controller(access_token)
    decode_content = response.body.decode("utf-8")
    content = json.loads(decode_content)

    assert response.status_code == 200
    assert content["status"] == "success"
    assert  content["data"] == fake_user.model_dump()
    
@pytest.mark.asyncio
async def test_get_current_user_error_UserNotFoundError(UserNotFoundOauth2Form):
    
    fake_token = at.create_access_token(UserNotFoundOauth2Form.username)
    
    #Error UserNotFoundError
    with pytest.raises(HTTPException) as error:
        user = await c.get_current_user_controller(fake_token)
    
    assert error.value.status_code == 404 #BAD REQUEST
    assert error.value.detail["status"] == "error"
    assert "message" in error.value.detail