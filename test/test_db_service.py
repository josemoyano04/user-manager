import pytest
from services import db_services as db

#============================== FIXTURES ==============================#
from test.common_fixtures import database_mock, updated_user_fixture, user_fixture

#============================== TEST ==============================#

@pytest.mark.asyncio
async def test_add_and_get_user(database_mock, user_fixture):
    await db.add_user(db_conn= database_mock, user= user_fixture)

    user = await  db.get_user(db_conn= database_mock, username= user_fixture.username)
    assert user is not None

@pytest.mark.asyncio
async def test_is_unique(database_mock, updated_user_fixture):
    unique = await db.is_unique(db_conn= database_mock,
                                user= updated_user_fixture,
                                for_update_user= True)
    assert unique
    
@pytest.mark.asyncio
async def test_update_user(database_mock, user_fixture, updated_user_fixture):
    await db.update_user(db_conn= database_mock, 
                         username= user_fixture.username, 
                         updated_user= updated_user_fixture)
    
    user = await db.get_user(db_conn= database_mock, 
                             username= updated_user_fixture.username,
                             visible_password= True)
    assert user is not None
    assert user.model_dump() == updated_user_fixture.model_dump()

@pytest.mark.asyncio
async def test_exists_username(database_mock, updated_user_fixture):
    exists = await db.exists_username(db_conn= database_mock,
                                      username= updated_user_fixture.username)    
    assert exists

@pytest.mark.asyncio
async def test_delete_user(database_mock, updated_user_fixture):
    await db.delete_user(db_conn= database_mock,
                         username= updated_user_fixture.username)
    
    user = await db.get_user(db_conn= database_mock,
                       username= updated_user_fixture.username)

    assert user is None
