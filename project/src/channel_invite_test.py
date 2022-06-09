from pytest import raises
from channel import channel_join, channel_invite, channel_leave
from channels import channels_create
from error import AccessError, InputError
from auth import auth_register
from other import clear

def test_channel_invite_assessing_1():
    result_1 = auth_register("vincent@gmail.com", "abc123abc123", "Vincent", "Lam")
    token1 = result_1['token']
    result_2 = auth_register("lam@gmail.com", "123abc123ABC", "Lam", "Vincent")
    u_id = result_2['u_id']
    result_3 = auth_register("vincentlam@gmail.com", "123ABC123abc", "VincentLam", "LamVincent")
    token2 = result_3['token']
    #Create channel
    name = "team1"
    is_public = True
    result = channels_create(token1,name,is_public)
    channel_id = result['channel_id']

    #User joins the channel
    channel_join(token2, channel_id)

    #invited the person who is invited
    #Assumptions, "Once invited the user is added to the channel immediately"
    #This would mean once the invite is done, they are "forced" in the channel
    #without any accepting of the invitations itself.
    channel_invite(token2,channel_id,u_id)

    #the second attempt to invite the second user, however nothing will happen
    channel_invite(token2,channel_id,u_id)


def test_channel_invite_assessing_2():
    clear()
    result_1 = auth_register("vincent@gmail.com", "abc123abc123", "Vincent", "Lam")
    token1 = result_1['token']
    result_2 = auth_register("lam@gmail.com", "123abc123ABC", "Lam", "Vincent")
    u_id = result_2['u_id']
    result_3 = auth_register("vincentlam@gmail.com", "123ABC123abc", "VincentLam", "LamVincent")
    token2 = result_3['token']
    #Create channel
    name = "team1"
    is_public = True
    result = channels_create(token1,name,is_public)
    channel_id = result['channel_id']

    #invited the second user cannot join due to the fact the first user does
    #not have access to the channel.
    #Assumptions, the user who was invited must be apart of the channel to invite
    #This a "AccessError"
    with raises(AccessError):
        assert channel_invite(token2, channel_id, u_id)


def test_channel_invite_assessing_3():
    clear()
    result_1 = auth_register("vincent@gmail.com", "abc123abc123", "Vincent", "Lam")
    token1 = result_1['token']
    result_2 = auth_register("lam@gmail.com", "123abc123ABC", "Lam", "Vincent")
    u_id = result_2['u_id']
    result_3 = auth_register("vincentlam@gmail.com", "123ABC123abc", "VincentLam", "LamVincent")
    token2 = result_3['token']
    #Create channel
    name = "team1"
    is_public = True
    result = channels_create(token1,name,is_public)
    channel_id = result['channel_id']

    #User joins the channel then leaves
    channel_join(token2, channel_id)
    channel_leave(token2, channel_id)

    #invited the second user cannot join due to the fact the first user does
    #not have access to the channel anymore after leaving the channel.
    #Assumptions, the user who was invited must be apart of the channel to invite
    #This a "AccessError"
    with raises(AccessError):
        assert channel_invite(token2, channel_id, u_id)

def test_channel_invite_type():
    clear()
    #Create channel
    x = auth_register("test@gmail.com", "easypass", "Nick", "Sal")
    t1 = x['token']
    name = "team1"
    is_public = True
    result = channels_create(t1,name,is_public)
    channel_id = result['channel_id']
    u_id = x['u_id']

    #Channel not valid
    #Error for wrong type
    with raises(InputError):
        assert channel_invite(t1, "String", u_id)

    #Error for float
    with raises(InputError):
        assert channel_invite(t1, 3.14, u_id)

    #Error for negatives
    with raises(InputError):
        assert channel_invite(t1, -1, u_id)

    #invited user not valid
    #Error for wrong type
    with raises(InputError):
        assert channel_invite(t1, channel_id, "String")

    #Error for float
    with raises(InputError):
        assert channel_invite(t1, channel_id, 3.14)

    #Error for negatives
    with raises(InputError):
        assert channel_invite(t1, channel_id, -1)

    #invalid token
    #Error for wrong type
    with raises(AccessError):
        assert channel_invite("string", channel_id, u_id)
