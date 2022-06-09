from channels import channels_create, channels_list, channels_listall
import pytest
from error import InputError, AccessError
from other import clear
from auth import auth_register

def test_channels_create():
    clear()
    #Create channel
    x = auth_register("test@gmail.com", "easypass", "Nick", "Sal")
    t1 = x['token']
    name = "team1"
    is_public = True
    assert(channels_create(t1,name,is_public) == {'channel_id': 0})

def test_channels_create_exc():
    clear()
    token = "incorrect"
    name = "team1"
    is_public = True
    with pytest.raises(AccessError):
        assert channels_create(token,name,is_public)

# test the user is only in one channel
def test_channels_list():
    clear()
    #Empty return
    x = auth_register("test@gmail.com", "easypass", "Nick", "Sal")
    t1 = x['token']
    assert (channels_list(t1) == {'channels': []})

# test the owner is not in any channel
def test_channels_list_exc():
    clear()
    token = "incorrect"
    with pytest.raises(AccessError):
        assert channels_list(token)

def test_channels_listall():
    clear()
    #Empty return
    x = auth_register("test@gmail.com", "easypass", "Nick", "Sal")
    t1 = x['token']
    assert (channels_listall(t1) == {'channels': []})

def test_channels_listall_exc():
    clear()
    token = "incorrect"
    with pytest.raises(AccessError):
        assert channels_listall(token)
    
def test_channels_createLongName():
    clear()
    x = auth_register("test@gmail.com", "easypass", "Nick", "Sal")
    t1 = x['token']
    with pytest.raises (InputError) :
        channels_create(t1,'jadhbiushdbvweqrweqrqwghjaevwgfhehehjvrbwjuhy',True)