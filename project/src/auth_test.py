''' This File is to test all functions in auth.py'''
import pytest
from auth import auth_login, auth_register, auth_logout, auth_passwordreset_request, auth_passwordreset_reset
from error import InputError, AccessError
auth_register("test@gmail.com", "1234567", "test", "test")

def test_valid_email_login():
    '''
    test for invalid email
    '''
    with pytest.raises(InputError):
        assert auth_login("notvalidemail.com", "1234567")

    with pytest.raises(InputError):
        assert auth_register("kanyewest.com", "1234567", "kanye", "west")
    
    with pytest.raises(InputError):
        assert auth_register("kanyewest.com", "1234567", "kanye", "west")
    
    with pytest.raises(InputError):
        assert auth_passwordreset_request("notvalidemail")

def test_used_email():
    '''
    test for used email
    '''
    with pytest.raises(InputError):
        assert auth_register("test@gmail.com", "1234567", "test", "test")

def test_wrong_password():
    '''
    test for wrong password
    '''
    with pytest.raises(InputError):
        assert auth_login("test@gmail.com", "2234567")

def test_unused_email_login():
    '''
    test for email not belonging to a user
    '''
    with pytest.raises(InputError):
        assert auth_login("unused@gmail.com", "1234567")

def test_failed_logout():
    '''
    test for failed logout
    '''
    with pytest.raises(AccessError):
        assert auth_logout("lOL")

def test_already_used_email():
    '''
    test for used email
    '''
    with pytest.raises(InputError):
        assert auth_register("test@gmail.com", "1234567", "test", "test")

def test_password_length():
    '''
    test for short password length
    '''
    with pytest.raises(InputError):
        assert auth_register("kanyewest@gmail.com", "LOL", "Kanye", "West")

def test_length_of_names():
    '''
    test for incorrect length names
    '''
    with pytest.raises(InputError):
        assert auth_register("kanyewest@gmail.com", "goodpassword123", "", "")

    with pytest.raises(InputError):
        assert auth_register("kanyewest@gmail.com", "goodpassword123",
                             "123456789012345678901234567890123456789901234567890123", "West")

def test_wrong_pass():
    '''
    test for incorrect password
    '''
    with pytest.raises(InputError):
        assert auth_login("coolguy69@gmail.com", "wrongpassword")

def test_wrong_username():
    '''
    test for incorrect username
    '''
    with pytest.raises(InputError):
        assert auth_login("notcoolguy69@gmail.com", "1234567")

def test_simple():
    with pytest.raises(InputError):
        auth_passwordreset_reset('string', "guy")

    with pytest.raises(InputError):
        auth_passwordreset_reset('string', "1234567")
