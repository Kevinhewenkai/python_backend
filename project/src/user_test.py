import pytest
from user import user_profile, user_profile_setname, user_profile_setemail, user_profile_sethandle
from auth import auth_register
from error import InputError, AccessError
from other import clear



def test_wrong_types():
    '''
    uid is not a valid user
    '''
    clear()
    token = auth_register("test@gmail.com", "1234567", "kanye", "west")['token']
    with pytest.raises(InputError):
        assert user_profile(token, 1.2)

    with pytest.raises(AccessError):
        assert user_profile(2, 2)

    with pytest.raises(InputError):
        assert user_profile(token, -12)

def test_invalid_token_uid():

    clear()
    login1 = auth_register("test@gmail.com", "1234567", "kanye", "west")
    uid = login1['u_id']
    token = login1['token']
    
    with pytest.raises(AccessError):
        assert user_profile("thisiswrong", uid)

    with pytest.raises(InputError):
        assert user_profile(token, 3)

def test_too_long():
    '''
    names character length
    '''
    clear()
    token = auth_register("test@gmail.com", "1234567", "kanye", "west")['token']
    with pytest.raises(InputError):
        user_profile_setname(token, "kanyekanyekanyekanyekanyekanyekanyekanyekanyekanye12", "West")

    with pytest.raises(InputError):
        user_profile_setname(token, "kanye", "WestWestWestWestWestWestWestWestWestWestWestWestWest")

def test_too_short():
    '''
    names character length
    '''
    clear()
    token = auth_register("test@gmail.com", "1234567", "kanye", "west")['token']
    with pytest.raises(InputError):
        assert user_profile_setname(token, "", "West")

    with pytest.raises(InputError):
        assert user_profile_setname(token, "Kanye", "")


def test_invalid_email():
    '''
    invalid email
    '''
    clear()
    token0 = auth_register('z5261340@gamil.com', 'lodasd', 'wenkai', 'he')['token']
    with pytest.raises(InputError):
        user_profile_setemail(token0, "1234567")

def test_same_email():
    clear()
    auth_register('z5261340@gamil.com', 'lodasd', 'wenkai', 'he')['token']
    token1 = auth_register('z5265555@gamil.com', 'lodasd', 'hwk', '123')['token']
    with pytest.raises(InputError):
        user_profile_setemail(token1, "z5261340@gamil.com")

# invalid handle
def test_short_handle():
    clear()
    token0 = auth_register('z5261340@gamil.com', 'lodasd', 'wenkai', 'he')['token']
    auth_register('z5265555@gamil.com', 'lodasd', 'hwk', '123')['token']
    with pytest.raises(InputError):
        user_profile_sethandle(token0, "hw")

def test_long_handle():
    clear()
    token0 = auth_register('z5261340@gamil.com', 'lodasd', 'wenkai', 'he')['token']
    auth_register('z5265555@gamil.com', 'lodasd', 'hwk', '123')['token']
    with pytest.raises(InputError):
        user_profile_sethandle(token0, "qwertyuiopasdfghjklzxcvbnm")

def test_same_handle():
    clear()
    token0 = auth_register('z5261340@gamil.com', 'lodasd', 'wenkai', 'he')['token']
    auth_register('z5265555@gamil.com', 'lodasd', 'hwk', '123')['token']
    with pytest.raises(InputError):
        user_profile_sethandle(token0, "hwk123")
