from channel import channel_join, channel_leave, channel_details
from channels import channels_create
from pytest import raises
from error import AccessError, InputError
from other import clear
from auth import auth_register

def test_channel_detail_assessing_1():
    #Create channel
    clear()
    x = auth_register("test@gmail.com", "easypass", "Nick", "Sal")
    t1 = x['token']
    name = "team1"
    is_public = True
    result = channels_create(t1,name,is_public)
    channel_id = result['channel_id']

    #User is trying to detail the channel without being apart of it
    #This is a access error
    y = auth_register("test2@gmail.com", "easypass", "Bob", "Sal")
    t2 = y['token']
    # channel_details(token2,channel_id)
    with raises(AccessError):
        assert channel_details(t2, channel_id)


def test_channel_detail_assessing_2():
    clear()
    #Create channel
    x = auth_register("test@gmail.com", "easypass", "Nick", "Sal")
    t1 = x['token']
    name = "team1"
    is_public = True
    result = channels_create(t1,name,is_public)
    channel_id = result['channel_id']

    #User joins the channel then leaves
    y = auth_register("test2@gmail.com", "easypass", "Bob", "Sal")
    t2 = y['token']
    channel_join(t2, channel_id)
    channel_details(t2,channel_id)
    channel_leave(t2, channel_id)

    #User is trying to detail the channel without being apart of it after
    #leaving it. This is a access error
    # channel_details(token2,channel_id)
    with raises(AccessError):
        assert channel_details(t2, channel_id)

def test_channel_details_type():
    #Create channel
    clear()
    x = auth_register("test@gmail.com", "easypass", "Nick", "Sal")
    t1 = x['token']
    name = "team1"
    is_public = True
    result = channels_create(t1,name,is_public)
    channel_id = result['channel_id']

    y = auth_register("test2@gmail.com", "easypass", "Bob", "Sal")
    t2 = y['token']

    #Error for wrong type
    with raises(InputError):
        assert channel_details(t2, "String")

    #Error for float
    with raises(InputError):
        assert channel_details(t2, 3.14)

    #Error for negatives
    with raises(InputError):
        assert channel_details(t2, -1)

    #Error for wrong token
    with raises(AccessError):
        assert channel_details("String", channel_id)
