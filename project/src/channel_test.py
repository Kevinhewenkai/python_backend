import pytest
from channel import channel_leave, channel_join, channel_addowner, channel_removeowner
from channels import channels_create
from auth import auth_register
from other import clear
from error import InputError, AccessError

def test_leave_except_input():
    clear()
    x = auth_register("test@gmail.com", "easypass", "Nick", "Sal")
    t1 = x['token']

    #InputError Tests
    with pytest.raises(InputError):
        assert channel_leave(t1, "Wrong Type")
    
    with pytest.raises(InputError):
        assert channel_leave(t1, 3.14159265)
    
    with pytest.raises(InputError):
        assert channel_leave(t1, -1)
    
    with pytest.raises(InputError):
        assert channel_leave(t1, 5)
    
def test_leave_except_access():
    clear()
    name = "Team 1"
    x = auth_register("test@gmail.com", "easypass", "Nick", "Sal")
    t1 = x['token']
    
    #AccessError Tests
    result = channels_create(t1, name, True)   
    channel_leave(t1, result['channel_id'])
    
    with pytest.raises(AccessError):
        assert channel_leave(t1, result['channel_id'])
        
def test_join_except():
    clear()
    name = "Team 1"
    x = auth_register("test@gmail.com", "easypass", "Nick", "Sal")
    y = auth_register("test2@gmail.com", "easypass", "Val", "Sal")
    t1 = x['token']
    t2 = y['token']
    
    #InputError Tests
    with pytest.raises(InputError):
        assert channel_join(t1, "Wrong Type")
    
    with pytest.raises(InputError):
        assert channel_join(t1, 3.14159265)
    
    with pytest.raises(InputError):
        assert channel_join(t1, -1)
    
    with pytest.raises(InputError):
        assert channel_join(t1, 5)
    
    #AccessError Tests *
    result = channels_create(t1, name, False)
    with pytest.raises(AccessError):
        assert channel_join(t2, result['channel_id'])
        
def test_addowner_except():
    clear()
    name = "Team 1"
    x = auth_register("test@gmail.com", "easypass", "Nick", "Sal")
    y = auth_register("test2@gmail.com", "easypass", "Val", "Sal")
    t1 = x['token']
    t2 = y['token']
    u1 = x['u_id']
    
    #InputError Tests *
    with pytest.raises(InputError):
        assert channel_addowner(t1, "Wrong Type", u1)
    
    with pytest.raises(InputError):
        assert channel_addowner(t1, 3.14159265, u1)
    
    with pytest.raises(InputError):
        assert channel_addowner(t1, -1, u1)
    
    with pytest.raises(InputError):
        assert channel_addowner(t1, 5, u1)
    
    result = channels_create(t1, name, True)
    with pytest.raises(InputError):
        assert channel_addowner(t1, result['channel_id'], u1)
    
    #Access Error Tests *
    channel_join(t2, result['channel_id'])
    with pytest.raises(AccessError):
        assert channel_addowner(t2, result['channel_id'], 1)
    
def test_removeowner_except():
    clear()
    x = auth_register("test@gmail.com", "easypass", "Nick", "Sal")
    t1 = x['token']
    u1 = x['u_id']
    
    #Input Error Tests *
    with pytest.raises(InputError):
        assert channel_removeowner(t1, "Wrong Type", u1)
    
    with pytest.raises(InputError):
        assert channel_removeowner(t1, 3.14159265, u1)
    
    with pytest.raises(InputError):
        assert channel_removeowner(t1, -1, u1)
    
    with pytest.raises(InputError):
        assert channel_removeowner(t1, 5, u1)
