from channels import channels_create
from channel import channel_join, channel_leave, channel_messages
from message import message_send, message_remove, message_react, message_unreact
from auth import auth_register, auth_passwordreset_request
from pytest import raises
from error import AccessError, InputError
from other import clear

#Create channel
def create_example_channel_1():
    x = auth_register("test@gmail.com", "easypass", "Vince", "Lam")
    token1 = x['token']
    name = "team1"
    is_public = True
    return channels_create(token1,name,is_public)['channel_id']


def test_channel_messages_assessing_1():
    clear()
    start = 50
    channel_id = create_example_channel_1()

    #Sending a message without authorisation
    y = auth_register("test2@gmail.com", "easypass", "Val", "Sal")
    token2 = y['token']

    with raises(AccessError):
        channel_messages(token2, channel_id, start)

def test_channel_messages_assessing_2():
    clear()
    start = 50
    #Create channel
    channel_id = create_example_channel_1()

    #User joins the channel and then leaves
    y = auth_register("test2@gmail.com", "easypass", "Val", "Sal")
    token2 = y['token']
    channel_join(token2, channel_id)
    message1 = "Sup Bro!"
    #Secondary test, test if the function will cause any errors if messages
    #is overloaded
    i = 0
    while i < 100:
        message_send(token2, channel_id, message1)
        i += 1
    channel_leave(token2, channel_id)

    with raises(AccessError):
        channel_messages(token2, channel_id, start)

def test_channel_messages_type():
    clear()
    start = 50
    channel_id = create_example_channel_1()
    y = auth_register("test2@gmail.com", "easypass", "Val", "Sal")
    token1 = y['token']
    #Error for wrong type
    with raises(InputError):
        channel_messages(token1, "String", start)

    #Error for float
    with raises(InputError):
        channel_messages(token1, 3.14, start)

    #Error for negatives
    with raises(InputError):
        channel_messages(token1, -1, start)

    #Error for wrong token
    with raises(AccessError):
        channel_messages("string", channel_id, start)

def test_channel_messages_size_1():
    clear()
    start = 50
    #Create channel
    channel_id = create_example_channel_1()
    #Error for start > end which is impossible AND testing for negative
    end = 20
    new_end = start - end
    y = auth_register("test2@gmail.com", "easypass", "Val", "Sal")
    token1 = y['token']
    with raises(AccessError):
        channel_messages(token1, channel_id, new_end)

#coverage increase
def test_channel_messages_assessing_3():
    clear()
    channel_id = create_example_channel_1()
    y = auth_register("test2@gmail.com", "easypass", "Val", "Sal")
    token2 = y['token']
    
    channel_join(token2, channel_id)
    
    message1 = "Sup Bro!"
    message_id = message_send(token2, channel_id, message1)['message_id']
    message2 = "what is your social security number?"
    message_send(token2, channel_id, message2)['message_id']
    start = 2
    channel_messages(token2, channel_id, start)
    message_remove(token2, message_id)
    start = 1
    channel_messages(token2, channel_id, start)

    channel_leave(token2, channel_id)

    auth_passwordreset_request("test2@gmail.com")

    with raises(AccessError):
        channel_messages(token2, channel_id, start)

def test_channel_messages_assessing_4():
    clear()
    react_id = 1
    channel_id = create_example_channel_1()
    y = auth_register("test2@gmail.com", "easypass", "Val", "Sal")
    token2 = y['token']
    
    channel_join(token2, channel_id)

    messages = 'sup'
    i = 0
    start = 1
    while i < 1000:
        message_id = message_send(token2, channel_id, messages)['message_id']
        message_react(token2, message_id, react_id)
        channel_messages(token2, channel_id, start)
        message_unreact(token2, message_id, react_id)
        channel_messages(token2, channel_id, start)
        i += 1
        start += 1
    start += 1

    with raises(AccessError):
        channel_messages(token2, channel_id, start)
