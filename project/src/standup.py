import time
import threading
import dataFile
from error import InputError, AccessError
from help_functions import decode_token, end_standup

def standup_start(token, channel_id, length):
    # token is valid
    if decode_token(token) == False:
        raise AccessError(description='Token is invalid')
    # channel_id is not valid
    if isinstance(channel_id, int) == False:
        raise InputError(description='Channel ID is not a valid channel')
    if channel_id >= dataFile.num_channels or channel_id < 0:
        raise InputError(description='Channel ID is not a valid channel')

    # An active standup is currently running in this channel
    if dataFile.data['channels'][channel_id]['is_standup_active'] == True:
        raise InputError(description='An active standup is currently running in this channel')
    
    now = int(time.time())
    time_finish = now + length
    
    dataFile.data['channels'][channel_id]['time_finish'] = time_finish
    dataFile.data['channels'][channel_id]['is_standup_active'] = True

    t = threading.Timer(length, end_standup, args=(token, channel_id))
    t.start()

    return {'time_finish': time_finish}

def standup_active(token, channel_id):
    # token is valid
    if decode_token(token) == False:
        raise AccessError(description='Token is invalid')
    # channel_id is not valid
    if isinstance(channel_id, int) == False:
        raise InputError(description='Channel ID is not a valid channel')
    if channel_id >= dataFile.num_channels or channel_id < 0:
        raise InputError(description='Channel ID is not a valid channel')

    is_active = dataFile.data['channels'][channel_id]['is_standup_active']
    time_finish = 0
    if is_active == False:
        time_finish = None
    else:
        time_finish = dataFile.data['channels'][channel_id]['time_finish']

    return {
        'is_active': is_active,
        'time_finish': time_finish
    }

def standup_send(token, channel_id, message):
    # token is valid
    if decode_token(token) == False:
        raise AccessError(description='Token is invalid')
    # channel_id is not valid
    if isinstance(channel_id, int) == False:
        raise InputError(description='Channel ID is not a valid channel')
    if channel_id >= dataFile.num_channels or channel_id < 0:
        raise InputError(description='Channel ID is not a valid channel')

     # An active standup is not currently running in this channel
    if dataFile.data['channels'][channel_id]['is_standup_active'] == False:
        raise InputError(
            'An active standup is not currently running in this channel')

    if len(message) > 1000:
        raise InputError(
            'Message is more Message is more than 1000 charactersthan 1000 characters')

    u_id = decode_token(token)['u_id']
    member_list = dataFile.data['channels'][channel_id]['members']
    
    if member_list.count(u_id) == 0:
        raise AccessError(
            'The authorised user is not a member of the channel that the message is within')

    first_name = dataFile.data['users'][u_id]['name_first']
    first_name += ': '
    message += '\n'
    result = first_name + message
    dataFile.data['channels'][channel_id]['standup_queue'] += result

    return {}