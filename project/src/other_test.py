import pytest
from auth import auth_register, auth_logout, auth_login
from error import InputError, AccessError
from other import clear, admin_userpermission_change, search, users_all
from help_functions import decode_token
from channel import channel_invite, channel_addowner, channel_leave, channel_removeowner, channel_join
from channels import channels_list
from message import message_edit, message_remove, message_send
from channels import channels_create
from user import user_profile, user_profile_setemail, user_profile_sethandle, user_profile_setname
from dataFile import data

#Create channel
def create_example_channel_1():
    clear()
    x = auth_register("test@gmail.com", "easypass", "Vince", "Lam")
    token1 = x['token']
    name = "team1"
    is_public = True
    return channels_create(token1,name,is_public)['channel_id']

def test_permission_change_exc():
    #Initialising data
    clear()

    x = auth_register("test@gmail.com", "easypass", "Nick", "Sal")
    y = auth_register("test2@gmail.com", "easypass", "Bob", "Sal")
    z = auth_register("test3@gmail.com", "easypass", "Fred", "Sal")

    token1 = x['token']
    t2 = y['token']

    u2 = y['u_id']
    u3 = z['u_id']

    #InputError Tests
    with pytest.raises(InputError):
        assert admin_userpermission_change(token1, "Wrong Type", 2)
    with pytest.raises(InputError):
        assert admin_userpermission_change(token1, u2, 3)
    with pytest.raises(InputError):
        assert admin_userpermission_change(token1, u2, "Wrong Type")
    with pytest.raises(InputError):
        assert admin_userpermission_change(token1, u2, 0)
    #AccessError Tests
    with pytest.raises(AccessError):
        assert admin_userpermission_change(t2, u3, 2)

def test_permission_change_return():
    #Initialising data
    clear()

    x = auth_register("test@gmail.com", "easypass", "Nick", "Sal")
    y = auth_register("test2@gmail.com", "easypass", "Bob", "Sal")
    z = auth_register("test3@gmail.com", "easypass", "Fred", "Sal")

    token1 = x['token']

    u2 = y['u_id']
    u3 = z['u_id']

    assert admin_userpermission_change(token1, u2, 1) == {}
    assert admin_userpermission_change(token1, u3, 2) == {}

def test_search_exc():
    clear()
    with pytest.raises(AccessError):
        assert search(-1, "Hello")

def test_search_return():
    #Initialising data
    clear()
    x = auth_register("test@gmail.com", "easypass", "Nick", "Sal")
    token1 = x['token']

    assert search(token1, "Test") == {'messages':[],}

#Two users, one creates channel, invite the other user, messages, changes messages, add other user as owner
#of channel, leaves channel, both user logs out, first user logs out twice and will raise input error.
def test_senario_1():
    clear()
    x = auth_register("test@gmail.com", "easypass", "Vince", "Lam")
    token1 = x['token']
    u_id_1 = decode_token(token1)['u_id']
    y = auth_register("testoken1@gmail.com", "easypassword", "Vincent", "Lam")
    token2 = y['token']
    u_id_2 = decode_token(token2)['u_id']
    auth_logout(token1)
    auth_login("test@gmail.com", "easypass")

    name = "team1"
    is_public = True
    channel_id = channels_create(token1,name,is_public)['channel_id']
    channels_list(token1)

    channel_invite(token1, channel_id, u_id_2)
    message = "Sup bro!"
    message_id = message_send(token1, channel_id, message)['message_id']
    newmessage = "Sup man!"
    message_edit(token1, message_id, newmessage)
    message_remove(token1, message_id)
    search(token1, message)
    
    user_info = user_profile(token1, u_id_1)
    name_first = user_info['user']['name_first']
    name_last = user_info['user']['name_last']
    email = user_info['user']['email']
    handle_str = user_info['user']['handle_str']
    user_profile_setname(token1, name_first + '2', name_last + '2')
    user_profile_setemail(token1, email[1:] + "C")
    user_profile_sethandle(token1, handle_str[1:] + "V")

    message2 = "THAT IS IDENITIY THEIF!!!"
    message_id = message_send(token2, channel_id, message2)['message_id']
    #1 User is checking user info of user 2
    channel_addowner(token1, channel_id, u_id_2)
    #He should be able to remove the original owner
    channel_removeowner(token2, channel_id, u_id_1)

    channel_leave(token1, channel_id)
    #Nothing should occur as leaving twice will no do anything
    channel_leave(token2, channel_id)

    #the first person should be owner of the channel since he is the first user.
    channel_join(token2, channel_id)
    #Nothing should happen if the user joins twice in a row
    channel_join(token2, channel_id)

    auth_logout(token1)
    auth_logout(token2)

    auth_login("est@gmail.comC", "easypass")
    with pytest.raises(AccessError):
        channel_leave(token1, channel_id)

def test_channel_coverage_increase():
    clear()
    #Create channel
    x = auth_register("test@gmail.com", "easypass", "Nick", "Sal")
    token1 = x['token']
    name = "team1"
    is_public = True
    result = channels_create(token1,name,is_public)
    channel_id = result['channel_id']
    u_id = x['u_id']

    user_info = user_profile(token1, u_id)
    name_first = user_info['user']['name_first']
    name_last = user_info['user']['name_last']
    handle_str = user_info['user']['handle_str']
    permission_id = data['users'][u_id]['permission_id']
    #token token not valid
    #Error for  type
    with pytest.raises(AccessError):
        assert channel_leave("string",channel_id)

    with pytest.raises(AccessError):
        assert channel_join("string",channel_id)

    with pytest.raises(AccessError):
        assert channel_addowner("string", channel_id, u_id)

    with pytest.raises(AccessError):
        assert channel_removeowner("string", channel_id, u_id)

    with pytest.raises(InputError):
        assert user_profile(token1, -1)

    with pytest.raises(AccessError):
        user_profile_setname("string", name_first, name_last)

    with pytest.raises(InputError):
        user_profile_setname(token1, "", name_last)
        
    with pytest.raises(AccessError):
        user_profile_sethandle("string", handle_str)

    with pytest.raises(InputError):
        user_profile_sethandle(token1, "he")

    with pytest.raises(AccessError):
        users_all("string")

    with pytest.raises(AccessError):
        admin_userpermission_change("string", u_id, permission_id)

    with pytest.raises(InputError):
        admin_userpermission_change(token1, -1, permission_id)

