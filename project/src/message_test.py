from channels import channels_create
from channel import channel_join, channel_leave
from message import message_send, message_edit, message_remove, message_pin, message_unpin, message_react, message_unreact, message_sendlater
from pytest import raises
from error import AccessError, InputError
from auth import auth_register
from other import clear
import time

#Create channel
def create_example_channel_1():
    x = auth_register("test@gmail.com", "easypass", "Vince", "Lam")
    token1 = x['token']
    name = "team1"
    is_public = True
    return channels_create(token1,name,is_public)['channel_id']
    
def test_messages_edit_assessing_1():
    clear()
    channel_id = create_example_channel_1()
    y = auth_register("test2@gmail.com", "easypass", "Val", "Sal")
    token2 = y['token']
    z = auth_register("test3@gmail.com", "easypass", "Fred", "Sal")
    token3 = z['token']

    channel_join(token2, channel_id)

    message2 = "what is your social security number?"
    message_id_2 = message_send(token2, channel_id, message2)['message_id']

    channel_leave(token2, channel_id)

    #editing message without authorisation after leaving the channel.
    message3 = "what is your phone number?"
    with raises(AccessError):
        message_edit(token3, message_id_2, message3)
    

def test_messages_edit_assessing_2():
    clear()
    channel_id = create_example_channel_1()
    y = auth_register("test2@gmail.com", "easypass", "Val", "Sal")
    token2 = y['token']
    z = auth_register("test3@gmail.com", "easypass", "Fred", "Sal")
    token3 = z['token']

    channel_join(token2, channel_id)

    message2 = "what is your social security number?"
    message_id_2 = message_send(token2, channel_id, message2)['message_id']

    channel_leave(token2, channel_id)

    # Given Assumptioon, creator of the message can still edit even though he left the channel
    message3 = "Can I get your number?"
    message_edit(token2, message_id_2, message3)

    #editing message without authorisation 
    message4 = "what is your phone number?"
    with raises(AccessError):
        message_edit(token3, message_id_2, message4)
    
def test_messages_remove_assessing_1():
    clear()
    channel_id = create_example_channel_1()
    y = auth_register("test2@gmail.com", "easypass", "Val", "Sal")
    token2 = y['token']
    z = auth_register("test3@gmail.com", "easypass", "Fred", "Sal")
    token3 = z['token']
    channel_join(token2, channel_id)

    message1 = "Sup Bro!"
    message_id_1 = message_send(token2, channel_id, message1)['message_id']
    message2 = "what is your social security number?"
    message_id_2 = message_send(token2, channel_id, message2)['message_id']
    message_remove(token2, message_id_2)

    channel_leave(token2, channel_id)

    with raises(AccessError):
        message_remove(token3, message_id_1)

def test_messages_remove_assessing_2():
    clear()
    x = auth_register("test@gmail.com", "easypass", "Vince", "Lam")
    token1 = x['token']
    name = "team1"
    is_public = True
    channel_id = channels_create(token1,name,is_public)['channel_id']

    y = auth_register("test2@gmail.com", "easypass", "Val", "Sal")
    token2 = y['token']
    
    channel_join(token2, channel_id)

    message1 = "Sup Bro!"
    message_id_1 = message_send(token1, channel_id, message1)['message_id']
    message2 = "what is your social security number?"
    message_id_2 = message_send(token2, channel_id, message2)['message_id']

    channel_leave(token2, channel_id)

    # Given Assumptioon, Owner can still edit the user 2 (token2), however user 2 cannot as he left.
    message_remove(token1, message_id_2)

    #Removing message without authorisation after leaving the channel.
    with raises(AccessError):
        message_remove(token2, message_id_1)

def test_messages_inputting_1():
    clear()
    channel_id = create_example_channel_1()
    y = auth_register("test2@gmail.com", "easypass", "Val", "Sal")
    token2 = y['token']
    
    channel_join(token2, channel_id)
    
    message1 = "Sup Bro!"
    message_id = message_send(token2, channel_id, message1)['message_id']
    message_remove(token2, message_id)

    #Removing a already removed message.
    with raises(InputError):
        message_remove(token2, message_id)

def test_messages_send_assessing_1():
    clear()
    channel_id = create_example_channel_1()
    
    #Sending a message without authorisation 
    y = auth_register("test2@gmail.com", "easypass", "Val", "Sal")
    token2 = y['token']
    message1 = "Sup Bro!"
    with raises(AccessError):
        message_send(token2, channel_id, message1)
  
def test_messages_send_assessing_2():
    clear()
    #Create channel
    channel_id = create_example_channel_1()
    
    #User joins the channel and then leaves
    y = auth_register("test2@gmail.com", "easypass", "Val", "Sal")
    token2 = y['token']
    channel_join(token2, channel_id)
    message1 = "Sup Bro!"
    message_send(token2, channel_id, message1)
    channel_leave(token2, channel_id)
    
    #Sending a message without authorisation after leaving
    message2 = "Sup Bro again!"
    with raises(AccessError):
        message_send(token2, channel_id, message2)

def test_messages_send_size():
    #Message is more than 1000 characters
    clear()
    channel_id = create_example_channel_1()
    y = auth_register("test2@gmail.com", "easypass", "Val", "Sal")
    token2 = y['token']
    message = ""
    x = 0
    while x < 1001:
        message = message + "A"
        x += 1
    with raises(InputError):
        message_send(token2 ,channel_id, message)
def test_messages_pin_unpin_assessing_1():
    clear()
    x = auth_register("test@gmail.com", "easypass", "Vince", "Lam")
    token1 = x['token']
    name = "team1"
    is_public = True
    channel_id = channels_create(token1,name,is_public)['channel_id']
    y = auth_register("test2@gmail.com", "easypass", "Val", "Sal")
    token2 = y['token']
    #z = auth_register("test3@gmail.com", "easypass", "Fred", "Sal")
    #token3 = z['token']
    channel_join(token2, channel_id)

    message1 = "Sup Bro!"
    message_id_1 = message_send(token2, channel_id, message1)['message_id']
    message2 = "what is your social security number?"
    message_id_2 = message_send(token2, channel_id, message2)['message_id']
    message_pin(token1,message_id_1)
    message_pin(token1,message_id_2)
    message_unpin(token1,message_id_1)

    #channel_leave(token2, channel_id)

    #Trying to unpin when leaving a channel
    with raises(AccessError):
        message_unpin(token2,message_id_2)

def test_messages_pin_unpin_assessing_2():
    clear()
    x = auth_register("test@gmail.com", "easypass", "Vince", "Lam")
    token1 = x['token']
    name = "team1"
    is_public = True
    channel_id = channels_create(token1,name,is_public)['channel_id']

    y = auth_register("test2@gmail.com", "easypass", "Val", "Sal")
    token2 = y['token']
    
    channel_join(token2, channel_id)

    message1 = "Sup Bro!"
    message_id_1 = message_send(token1, channel_id, message1)['message_id']
    message2 = "what is your social security number?"
    message_id_2 = message_send(token2, channel_id, message2)['message_id']
    message_pin(token1,message_id_1)
    message_pin(token1,message_id_2)

    channel_leave(token2, channel_id)

    #Given Assumptioon, Owner can still unpin the user 2 (token2), however user 2 cannot as he left.
    message_unpin(token1,message_id_1)

    #Pinning message without authorisation after leaving the channel.
    with raises(AccessError):
        message_pin(token2,message_id_1)

def test_messages_pin_unpin_inputting_1():
    clear()
    x = auth_register("test@gmail.com", "easypass", "Vince", "Lam")
    token1 = x['token']
    name = "team1"
    is_public = True
    channel_id = channels_create(token1,name,is_public)['channel_id']
    y = auth_register("test2@gmail.com", "easypass", "Val", "Sal")
    token2 = y['token']
    
    channel_join(token2, channel_id)
    
    message1 = "Sup Bro!"
    message_id = message_send(token2, channel_id, message1)['message_id']
    message2 = "what is your social security number?"
    message_id_2 = message_send(token2, channel_id, message2)['message_id']
    message_remove(token2, message_id)

    #pinning a already removed message.
    with raises(InputError):
        message_pin(token2, message_id)

    #Pinning a already pinned message.
    message_pin(token1, message_id_2)
    with raises(InputError):
        message_pin(token1, message_id_2)

    #unpinning a already removed message.
    with raises(InputError):
        message_unpin(token2, message_id)

    #Pinning a already pinned message.
    message_unpin(token1, message_id_2)
    with raises(InputError):
        message_unpin(token1, message_id_2)

    with raises(AccessError):
        message_unpin('string', message_id)

    with raises(AccessError):
        message_unpin(3.14, message_id)
    
    with raises(AccessError):
        message_unpin(-1, message_id)
    
    with raises(InputError):
        message_unpin(token2, 'string')

    with raises(InputError):
        message_unpin(token2, 3.14)
    
    with raises(InputError):
        message_unpin(token2, -1)

    with raises(AccessError):
        message_pin('string', message_id)

    with raises(AccessError):
        message_pin(3.14, message_id)
    
    with raises(AccessError):
        message_pin(-1, message_id)
    
    with raises(InputError):
        message_pin(token2, 'string')

    with raises(InputError):
        message_pin(token2, 3.14)
    
    with raises(InputError):
        message_pin(token2, -1)

def test_messages_react_unreact_assessing_1():
    clear()
    channel_id = create_example_channel_1()
    y = auth_register("test2@gmail.com", "easypass", "Val", "Sal")
    token2 = y['token']
    #z = auth_register("test3@gmail.com", "easypass", "Fred", "Sal")
    #token3 = z['token']
    channel_join(token2, channel_id)

    message1 = "Sup Bro!"
    message_id_1 = message_send(token2, channel_id, message1)['message_id']
    message2 = "what is your social security number?"
    message_id_2 = message_send(token2, channel_id, message2)['message_id']
    react_id = 1
    message_react(token2,message_id_1, react_id)
    message_react(token2,message_id_2, react_id)
    message_unreact(token2,message_id_1, react_id)

    channel_leave(token2, channel_id)

    #Trying to unpin when leaving a channel
    with raises(InputError):
        message_unreact(token2, message_id_1, react_id)

def test_messages_react_unreact_assessing_2():
    clear()
    x = auth_register("test@gmail.com", "easypass", "Vince", "Lam")
    token1 = x['token']
    name = "team1"
    is_public = True
    channel_id = channels_create(token1,name,is_public)['channel_id']

    y = auth_register("test2@gmail.com", "easypass", "Val", "Sal")
    token2 = y['token']
    
    channel_join(token2, channel_id)

    message1 = "Sup Bro!"
    message_id_1 = message_send(token1, channel_id, message1)['message_id']
    message2 = "what is your social security number?"
    message_id_2 = message_send(token2, channel_id, message2)['message_id']
    react_id = 1
    message_react(token2,message_id_1, react_id)
    message_react(token2,message_id_2, react_id)

    channel_leave(token2, channel_id)

    #Pinning message without authorisation after leaving the channel.
    with raises(InputError):
        message_react(token2,message_id_1, react_id)

def test_messages_react_unreact_inputting_1():
    clear()
    channel_id = create_example_channel_1()
    y = auth_register("test2@gmail.com", "easypass", "Val", "Sal")
    token2 = y['token']
    
    channel_join(token2, channel_id)
    
    message1 = "Sup Bro!"
    message_id = message_send(token2, channel_id, message1)['message_id']
    message2 = "what is your social security number?"
    message_id_2 = message_send(token2, channel_id, message2)['message_id']
    message_remove(token2, message_id)

    react_id = 1
    #pinning a already removed message.
    with raises(InputError):
        message_react(token2, message_id, react_id)

    #Pinning a already pinned message.
    message_react(token2, message_id_2, react_id)
    with raises(InputError):
        message_react(token2, message_id_2, react_id)

    #unpinning a already removed message.
    with raises(InputError):
        message_unreact(token2, message_id, react_id)

    #Pinning a already pinned message.
    message_unreact(token2, message_id_2, react_id)
    with raises(InputError):
        message_unreact(token2, message_id_2, react_id)

    with raises(AccessError):
        message_unreact('string', message_id, react_id)

    with raises(AccessError):
        message_unreact(3.14, message_id, react_id)
    
    with raises(AccessError):
        message_unreact(-1, message_id, react_id)
    
    with raises(InputError):
        message_unreact(token2, 'string', react_id)

    with raises(InputError):
        message_unreact(token2, 3.14, react_id)
    
    with raises(InputError):
        message_unreact(token2, -1, react_id)

    with raises(InputError):
        message_unreact(token2, message_id_2, 'string')

    with raises(InputError):
        message_unreact(token2, message_id_2, 3.14)

    with raises(InputError):
        message_unreact(token2, message_id_2, -1)

    with raises(InputError):
        message_unreact(token2, message_id_2, react_id)

    with raises(AccessError):
        message_react('string', message_id, react_id)

    with raises(AccessError):
        message_react(3.14, message_id, react_id)
    
    with raises(AccessError):
        message_react(-1, message_id, react_id)
    
    with raises(InputError):
        message_react(token2, 'string', react_id)

    with raises(InputError):
        message_react(token2, 3.14, react_id)
    
    with raises(InputError):
        message_react(token2, -1, react_id)

    with raises(InputError):
        message_react(token2, message_id_2, 'string')

    with raises(InputError):
        message_react(token2, message_id_2, 3.14)

    with raises(InputError):
        message_react(token2, message_id_2, -1)

#Coverage Increase

def test_messages_sendlater_1():
    clear()
    channel_id = create_example_channel_1()
    y = auth_register("test2@gmail.com", "easypass", "Val", "Sal")
    token2 = y['token']
    
    channel_join(token2, channel_id)
    
    time_sent = int(time.time()) + 10
    message1 = "Sup Bro!"
    message_sendlater(token2, channel_id, message1, time_sent)['message_id']
    message2 = "what is your social security number?"
    message_sendlater(token2, channel_id, message2, time_sent)['message_id']
    
    channel_leave(token2, channel_id)

    message3 = "what is your phone number?"
    #Removing a already removed message.
    with raises(AccessError):
        message_sendlater(token2, channel_id, message3, time_sent)['message_id']

def test_messages_sendlater_size():
    clear()
    channel_id = create_example_channel_1()
    
    #Sending a message without authorisation 
    y = auth_register("test2@gmail.com", "easypass", "Val", "Sal")
    token2 = y['token']
    message2 = "a" * 10000
    time_sent = int(time.time()) + 10
    with raises(InputError):
        message_sendlater(token2, channel_id, message2, time_sent)

def test_message_inputting():
    clear()
    channel_id = create_example_channel_1()
    y = auth_register("test2@gmail.com", "easypass", "Val", "Sal")
    token2 = y['token']
    
    channel_join(token2, channel_id)
    
    message1 = "Sup Bro!"
    message_id = message_send(token2, channel_id, message1)['message_id']
    message2 = "what is your social security number?"
    message_id_2 = message_send(token2, channel_id, message2)['message_id']
    message_remove(token2, message_id)

    with raises(AccessError):
        message_send('string', channel_id, message1)

    with raises(AccessError):
        message_send(3.14, channel_id, message1)

    with raises(AccessError):
        message_send(-1, channel_id, message1)

    with raises(InputError):
        message_send(token2, 'string', message1)

    with raises(InputError):
        message_send(token2, 3.14, message1)
    
    with raises(InputError):
        message_send(token2, -1, message1)

    with raises(AccessError):
        message_remove('string', message_id)
    
    with raises(AccessError):
        message_remove(3.14, message_id_2)

    with raises(AccessError):
        message_remove(-1, message_id)

    with raises(InputError):
        message_remove(token2, {})
    
    time_sent = int(time.time()) + 10
    with raises(AccessError):
        message_sendlater('string', channel_id, message1, time_sent)

    with raises(AccessError):
        message_sendlater(3.14, channel_id, message1, time_sent)

    with raises(AccessError):
        message_sendlater(-1, channel_id, message1, time_sent)

    with raises(InputError):
        message_sendlater(token2, 'string', message1, time_sent)

    with raises(InputError):
        message_sendlater(token2, 3.14, message1, time_sent)

    with raises(InputError):
        message_sendlater(token2, -1, message1, time_sent)
    
    with raises(InputError):
        message_sendlater(token2, channel_id, message1, -1)
