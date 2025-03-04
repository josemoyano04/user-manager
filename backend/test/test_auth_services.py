import pytest
import services.db_services as db 
import services.auth_services as at
import services.hashing_service as hs 
from models.user_db import UserDB
from models.responses.token_response import Token
from errors.users_errors import UserNotFoundError
from fastapi.security import OAuth2PasswordRequestForm

#=======================================FIXTURES=======================================
at.login_for_access_token#
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


#=======================================TESTS=======================================
@pytest.mark.asyncio
async def test_authenticate_user(create_data_in_database):
    
    auth1 = await at.authenticate_user(username= "userTest", password= "testing")  
    auth2 = await at.authenticate_user(username= "userTest", password= "fakePass")
    assert auth1 is True
    assert auth2 is False
    
    with pytest.raises(UserNotFoundError):
        await at.authenticate_user(username= "Fake Username", password= "Fake password")    

@pytest.mark.asyncio
async def test_login_for_access_token(Oauth2Form, UserNotFoundOauth2Form):
    token = await at.login_for_access_token(form_data= Oauth2Form)
    assert isinstance(token, Token)

    with pytest.raises(UserNotFoundError):
        await at.login_for_access_token(form_data= UserNotFoundOauth2Form)
        

@pytest.mark.asyncio
async def test_get_current_user(Oauth2Form, fake_user):
    token = await at.login_for_access_token(form_data= Oauth2Form)
    user: UserDB = await at.get_current_user(token= token.token)
    
    assert user is not None
    assert user.full_name == fake_user.full_name
    assert user.username == fake_user.username
    assert user.email == fake_user.email