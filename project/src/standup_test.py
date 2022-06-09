from channels import channels_create
from channel import channel_join, channel_leave, channel_messages
from message import message_send, message_remove, message_react, message_unreact
from auth import auth_register
from pytest import raises
from error import AccessError, InputError
from other import clear
from standup import standup_start, standup_send, standup_active
from time import sleep

#Create channel
def create_example_channel_1():
    x = auth_register("test@gmail.com", "easypass", "Vince", "Lam")
    token1 = x['token']
    name = "team1"
    is_public = True
    return channels_create(token1,name,is_public)['channel_id']

def test_active_token_error():
    clear()
    x = auth_register("test@gmail.com", "easypass", "Nick", "Sal")
    token = x['token']
    x = channels_create(token, 'team1', False)
    channel_id = x['channel_id']
    with raises(AccessError):
        standup_active("incorrect", channel_id)


def test_active_channelId_error():
    clear()
    x = auth_register("test@gmail.com", "easypass", "Nick", "Sal")
    token = x['token']
    with raises(InputError):
        standup_active(token, 45646)


def test_active_channelId_int_error():
    clear()
    x = auth_register("test@gmail.com", "easypass", "Nick", "Sal")
    token = x['token']
    with raises(InputError):
        standup_active(token, 2.153123)


def test_start_twice_active_error():
    clear()
    x = auth_register("test@gmail.com", "easypass", "Nick", "Sal")
    token = x['token']
    x = channels_create(token, 'team1', False)
    channel_id = x['channel_id']
    standup_start(token, channel_id, 10)
    with raises(InputError):
        standup_start(token, channel_id, 10)


def test_start_token_error():
    clear()
    x = auth_register("test@gmail.com", "easypass", "Nick", "Sal")
    token = x['token']
    x = channels_create(token, 'team1', False)
    channel_id = x['channel_id']
    with raises(AccessError):
        standup_start("incorrect", channel_id, 10)


def test_start_channelId_error():
    clear()
    x = auth_register("test@gmail.com", "easypass", "Nick", "Sal")
    token = x['token']
    with raises(InputError):
        standup_start(token, 45646, 10)


def test_start_channelId_int_error():
    clear()
    x = auth_register("test@gmail.com", "easypass", "Nick", "Sal")
    token = x['token']
    with raises(InputError):
        standup_start(token, 2.153123, 10)


def test_send_message_error():
    clear()
    x = auth_register("test@gmail.com", "easypass", "Nick", "Sal")
    token = x['token']
    x = channels_create(token, 'team1', False)
    channel_id = x['channel_id']
    message = ""
    i = 0
    while i <= 1000:
        message += 'aaa'
        i += 1
    standup_start(token, channel_id, 10)
    with raises(InputError):
        standup_send(token, channel_id, message)


def test_send_token_error():
    clear()
    x = auth_register("test@gmail.com", "easypass", "Nick", "Sal")
    token = x['token']
    x = channels_create(token, 'team1', False)
    channel_id = x['channel_id']
    message = 'kevin so handsome'
    with raises(AccessError):
        standup_send("incorrect", channel_id, message)


def test_send_channelId_error():
    clear()
    x = auth_register("test@gmail.com", "easypass", "Nick", "Sal")
    token = x['token']
    message = 'kevin so handsome'
    x = channels_create(token, 'team1', False)
    channel_id = x['channel_id']
    standup_start(token, channel_id, 10)
    with raises(InputError):
        standup_send(token, 45646, message)


def test_send_channelId_int_error():
    clear()
    x = auth_register("test@gmail.com", "easypass", "Nick", "Sal")
    token = x['token']
    message = 'kevin so handsome'
    x = channels_create(token, 'team1', False)
    channel_id = x['channel_id']
    standup_start(token, channel_id, 10)
    with raises(InputError):
        standup_send(token, 2.1516, message)

def test_send_active_error():
    clear()
    x = auth_register("test@gmail.com", "easypass", "Nick", "Sal")
    token = x['token']
    x = channels_create(token, 'team1', False)
    channel_id = x['channel_id']
    message = 'kevin so handsome'
    with raises(InputError):
        standup_send(token, channel_id, message)

def test_send_user_error():
    clear()
    x = auth_register("test@gmail.com", "easypass", "Nick", "Sal")
    token1 = x['token']
    x = auth_register("test22@gmail.com", "easypasssss", "Nickkk", "Salll")
    token2 = x['token']
    x = channels_create(token1, 'team1', False)
    channel_id = x['channel_id']
    standup_start(token1, channel_id, 10)
    message = 'kevin so handsome'
    with raises(AccessError):
        standup_send(token2, channel_id, message)

def test_standup_inputting_1():
    clear()
    time = 1
    channel_id = create_example_channel_1()
    y = auth_register("test2@gmail.com", "easypass", "Val", "Sal")
    token1 = y['token']
    message = "sup"
    channel_join(token1, channel_id)
    #Error for wrong type
    with raises(AccessError):
        standup_send('string', channel_id, message)

    #Error for float
    with raises(AccessError):
        standup_send(3.14, channel_id, message)

    #Error for negatives
    with raises(AccessError):
        standup_send(-1, channel_id, message)

    #Error for wrong token
    with raises(InputError):
        standup_send(token1, 'string', message)

    with raises(InputError):
        standup_send(token1, 3.14, message)

    with raises(InputError):
        standup_send(token1, -1, message)

    message = "SUP" * 10000
    with raises(InputError):
        standup_send(token1, channel_id, message)

    with raises(InputError):
        standup_send(token1, channel_id, 'string')

    with raises(InputError):
        standup_send(token1, channel_id, 3.14)

    with raises(InputError):
        standup_send(token1, channel_id, -1)

    with raises(AccessError):
        standup_start('string', channel_id, time)

    with raises(AccessError):
        standup_start(3.14, channel_id, time)

    with raises(AccessError):
        standup_start(-1, channel_id, time)

    with raises(InputError):
        standup_start(token1, 'string', time)

    with raises(InputError):
        standup_start(token1, 3.14, time)

    with raises(InputError):
        standup_start(token1, -1, time)

    with raises(AccessError):
        standup_active('string', channel_id)

    with raises(AccessError):
        standup_active(3.14, channel_id)

    with raises(AccessError):
        standup_active(-1, channel_id)

    with raises(InputError):
        standup_active(token1, 'string')

    with raises(InputError):
        standup_active(token1, 3.14)

    with raises(InputError):
        standup_active(token1, -1)

