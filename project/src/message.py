import dataFile
import time
import threading
from help_functions import decode_token, message_future, message_find, message_find_react, reacts, pin
from error import InputError
from error import AccessError

def message_send(token, channel_id, message):
    if decode_token(token) == False:
        raise AccessError(description='Token is invalid')
    if isinstance(channel_id, int) == False:
        raise InputError(description='Channel ID is not a valid channel')
    if channel_id >= dataFile.num_channels or channel_id < 0:
        raise InputError(description='Channel ID is not a valid channel')
    
    message_list = dataFile.data['channels'][channel_id]['messages']
    member_list = dataFile.data['channels'][channel_id]['members']
    
    if len(message) > 1000:
        raise InputError(description='Message is more Message is more than 1000 charactersthan 1000 characters')
    
    u_id = decode_token(token)['u_id']
    
    if member_list.count(u_id) == 0:
        raise AccessError(description='Authorised user is not a member of channel with channel_id')
    
    now = int(time.time())
    dataFile.num_messages_created += 1
    detail = {
        'message_id': dataFile.num_messages_created,
        'u_id': u_id,
        'message': message,
        'time_created': now,
        'is_pinned': False,
        'reacts' : [{
            'react_id' : 1,
            'u_ids' : [],
            'is_this_user_reacted' : False,
        }]
    }
    dataFile.data['channels'][channel_id]['total_messages'] += 1
    message_list.append(detail)
    message_id = detail["message_id"]
 
    return {'message_id':message_id}

def message_remove(token, message_id):
    #Assuptions, when removing the messages it also updates the "time_created" to the current time.
    if decode_token(token) == False:
        raise AccessError(description ='Token is invalid')
    
    u_id = decode_token(token)['u_id']
    permission = dataFile.data['users'][u_id]['permission_id']

    exists = False
 
    for channel in dataFile.data['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                exists = True
                if message['u_id'] != u_id and permission == 2 and channel['owners'].count(u_id) == 0:
                    raise AccessError(description ='Message was not sent by authorised user and there is no owner status')
                channel['messages'].remove(message)
                break
        else:
            continue
        break    
    
    if exists == False:       
        raise InputError(description ='Message with message_id does not exist')
    
    return {
    }

def message_edit(token, message_id, message):
    if decode_token(token) == False:
        raise AccessError(description ='Token is invalid')

    u_id = decode_token(token)['u_id']
    permission = dataFile.data['users'][u_id]['permission_id']
    
    #Assuptions, when editing the messages it also updates the "time_created" to the current time.
    now = int(time.time())
    
    for channel in dataFile.data['channels']:
        for item in channel['messages']:
            if item['message_id'] == message_id:
                if item['u_id'] != u_id and permission == 2 and channel['owners'].count(u_id) == 0:
                    raise AccessError(description ='Message was not sent by authorised user and and there is no owner status')
                if len(message) == 0:
                    channel['total_messages'] -= 1
                    channel['messages'].remove(item)
                else:
                    item['message'] = message
                    item['time_created'] = now
    
    return {}

def message_sendlater(token, channel_id, message, time_sent):
    now = int(time.time())
    if decode_token(token) == False:
        raise AccessError(description ='Token is invalid')
    if isinstance(channel_id, int) == False:
        raise InputError(description ='Channel ID is not a valid channel')
    if channel_id >= dataFile.num_channels or channel_id < 0:
        raise InputError(description ='Channel ID is not a valid channel')
    if time_sent < now:
        raise InputError(description ='Time sent is a time in the past')

    member_list = dataFile.data['channels'][channel_id]['members']
    
    if len(message) > 1000:
        raise InputError(description ='Message is more than 1000 characters')
    
    u_id = decode_token(token)['u_id']

    if member_list.count(u_id) == 0:
        raise AccessError(description ='Authorised user is not a member of channel with channel_id')
    
    dataFile.num_messages_created += 1
    seconds = int(time_sent - now)
    t = threading.Timer(seconds, message_future, args=(token, channel_id, message))
    t.start()

    return {'message_id':dataFile.num_messages_created}

def message_react(token, message_id, react_id):
    if decode_token(token) == False:
        raise AccessError(description='Token is invalid')
    if isinstance(message_id, int) == False:
        raise InputError(description='message_id is not a valid message')
    if isinstance(react_id, int) == False:
        raise InputError(description='react_id is not a valid React ID')
    
    u_id = decode_token(token)['u_id']
    permission = dataFile.data['users'][u_id]['permission_id']
    
    message = message_find_react(message_id, u_id, permission, react_id)
    react = reacts(message, react_id)
    if react == False:
        raise InputError(description='react_id is not a valid React ID')

    if react['u_ids'].count(u_id) > 0:
        raise InputError("Message with ID message_id already contains an active React with ID react_id from the authorised user") 
    else:
        react['u_ids'].append(u_id)
    return {}

def message_unreact(token, message_id, react_id):
    if decode_token(token) == False:
        raise AccessError(description='Token is invalid')
    
    u_id = decode_token(token)['u_id']
    
    if isinstance(message_id, int) == False:
        raise InputError(description='message_id is not a valid message')

    if isinstance(react_id, int) == False:
        raise InputError(description='react_id is not a valid React ID')
    
    permission = dataFile.data['users'][u_id]['permission_id']
    
    message = message_find_react(message_id, u_id, permission, react_id)
    react = reacts(message, react_id)
    if react == False:
        raise InputError(description='react_id is not a valid React ID')
    
    if react['u_ids'].count(u_id) > 0:
        react['u_ids'].remove(u_id)
    else:
        raise InputError("Message with ID message_id does not contain an active React with ID react_id") 
    return {}

def message_pin(token, message_id):
    if decode_token(token) == False:
        raise AccessError(description='Token is invalid')
    if isinstance(message_id, int) == False:
        raise InputError(description='message_id is not a valid message')
    if dataFile.num_messages_created < message_id:
        raise InputError(description='message_id is not a valid message')
    
    u_id = decode_token(token)['u_id']
    permission = dataFile.data['users'][u_id]['permission_id']

    if isinstance(message_id, int) == False:
        raise InputError(description='message_id is not a valid message')

    message = message_find(message_id, u_id, permission)
    pinning = True
    pin(message, pinning)
    return {}

def message_unpin(token, message_id):
    if decode_token(token) == False:
        raise AccessError(description='Token is invalid')
    if isinstance(message_id, int) == False:
        raise InputError(description='message_id is not a valid message')
    if dataFile.num_messages_created < message_id:
        raise InputError(description='message_id is not a valid message')
    
    u_id = decode_token(token)['u_id']
    permission = dataFile.data['users'][u_id]['permission_id']
    message = message_find(message_id, u_id, permission)
    pinning = False
    pin(message, pinning)
    return {}
