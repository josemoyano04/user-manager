import pytest
import services.hashing_service as hs


def test_hashing_and_validate_password():
    password = "example"
    hash = hs.hashed_password(password) 
    
    assert hs.validate_password(password, hash)
    
    fake_password = "fake example"
    assert hs.validate_password(fake_password, hash) is False