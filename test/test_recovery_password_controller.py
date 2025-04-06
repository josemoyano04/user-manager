import pytest
from fastapi import HTTPException
from utils.env_loader import EnvManager
from models.request.validate_code_request import ValidateRecoveryCodeRequest
from models.request.generate_code_request import RecoveryPasswordRequest
from services.db_services import add_user, get_user_by_email
from test.common_fixtures import database_mock, user_with_hashed_password_fixture
from controllers.recovery_user_password_controller import (generate_and_send_code_controller, 
                                                           updated_password_controller,
                                                           validate_code_controller)

# ==================== FIXTURES ====================
@pytest.fixture(scope= 'module')
def recovery_pass_request():
    #data
    env = EnvManager()
    sender = env.get("SENDER_EMAIL")
    password = env.get("PASSWORD_EMAIL")
    
    return RecoveryPasswordRequest(password_email= password,
                                   sender_email= sender,
                                   receiver_email= sender)

@pytest.fixture(scope= 'module')  
def recovery_pass_request_with_code(recovery_pass_request):
    copy = recovery_pass_request.model_copy()
    copy.custom_code = "12345"
    return copy
    
@pytest.fixture(scope= 'module')
def recovery_pass_request_with_unregistered_email(recovery_pass_request):
    copy = recovery_pass_request.model_copy()
    copy.receiver_email = "unregistedEmail@example.com"
    return copy

@pytest.fixture(scope= 'module')
def validated_code_request(recovery_pass_request_with_code):
    return ValidateRecoveryCodeRequest( code= recovery_pass_request_with_code.custom_code,
                                        user_email= recovery_pass_request_with_code.receiver_email)

@pytest.fixture(scope= 'module')
def validate_code_request_with_fake_code(validated_code_request):
    copy = validated_code_request.model_copy()
    copy.code = "fake_code"
    return copy
    

@pytest.fixture(scope= "module")
async def add_data_in_database(database_mock, user_with_hashed_password_fixture):
    user_with_hashed_password_fixture.email = EnvManager().get("SENDER_EMAIL")
    await add_user(db_conn= database_mock, user= user_with_hashed_password_fixture)
    
    
# ==================== TEST ====================
@pytest.mark.asyncio
async def test_generate_and_send_code_controller(recovery_pass_request,
                                                 recovery_pass_request_with_unregistered_email,
                                                 database_mock,
                                                 add_data_in_database):
    
    response = await generate_and_send_code_controller(db_conn= database_mock,
                                                    recovery_password_request= recovery_pass_request)
    assert response.status_code == 200, "Status code is not 200"
    
    with pytest.raises(HTTPException) as excinfo:
        response = await generate_and_send_code_controller(db_conn= database_mock,
                                                         recovery_password_request= recovery_pass_request_with_unregistered_email)

    assert excinfo.value.status_code == 404, "Status code is not 404"
    
@pytest.mark.asyncio
async def test_validate_code_controller(database_mock, add_data_in_database, 
                                        recovery_pass_request_with_code, validated_code_request,
                                        validate_code_request_with_fake_code):
    
    await generate_and_send_code_controller(db_conn= database_mock,
                                            recovery_password_request= recovery_pass_request_with_code)
    
    with pytest.raises(HTTPException) as excinfo:
        response = await validate_code_controller(db_conn= database_mock,
                                                  validate_code_request= validate_code_request_with_fake_code)
    
    assert excinfo.value.status_code == 400, "Status code is not 400"
    
    response = await validate_code_controller(db_conn= database_mock,
                                              validate_code_request= validated_code_request)
    
    assert response.status_code == 200, "Status code is not 200"
    