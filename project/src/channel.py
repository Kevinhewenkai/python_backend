import dataFile
from error import InputError, AccessError
from help_functions import decode_token

def channel_details(token, channel_id):
    if decode_token(token) == False:
        raise AccessError(description ='Token is invalid')
    if isinstance(channel_id, int) == False:
        raise InputError(description ='Channel ID is not an integer')
    if channel_id >= dataFile.num_channels or channel_id < 0:
        raise InputError(description ='Channel ID is not a valid channel')

    owner_list = dataFile.data['channels'][channel_id]['owners']
    member_list = dataFile.data['channels'][channel_id]['members']
    channel_name = dataFile.data['channels'][channel_id]['name']
    
    auth_user = decode_token(token)['u_id']
    if member_list.count(auth_user) == 0:
        raise AccessError(description ='Authorised user is not a member of channel with channel id')
    
    details = {
        'name': channel_name,
        'owner_members': [],
        'all_members': [],
    }
    if len(owner_list) > 0:
        for user in owner_list:
            details['owner_members'].append(dataFile.data['users'][user])
    
    if len(member_list) > 0:
        for user in member_list:
            details['all_members'].append(dataFile.data['users'][user])
    
    return details
    
def channel_messages(token, channel_id, start):
    if decode_token(token) == False:
        raise AccessError('Token is invalid')
    if isinstance(channel_id, int) == False:
        raise InputError('Channel ID is not a valid channel')
    if channel_id >= dataFile.num_channels or channel_id < 0:
        raise InputError('Channel ID is not a valid channel')
    
    auth_user = decode_token(token)['u_id']
    member_list = dataFile.data['channels'][channel_id]['members']
    message_list = dataFile.data['channels'][channel_id]['messages']
    total_messages = dataFile.data['channels'][channel_id]['total_messages']
    
    if member_list.count(auth_user) == 0:
        raise AccessError('Authorised user is not already a member of the channel')
    
    if start > total_messages:
        raise AccessError('Start is greater than the total number of messages in the channel')
    
    if start + 50 < total_messages:
        end = start + 50
    else:
        end = -1
    
    if end == -1:
        length = total_messages
    else:
        length = end
    #Assumptions, Although it was not required assume that there is more than one react_id (eg, 1, 2, 3, 4)
    
    for message in message_list:
        for reacts in message['reacts']: #Hence, the for loops.
            reacts['is_this_user_reacted'] = False
            if reacts['u_ids'].count(auth_user) > 0:
                reacts['is_this_user_reacted'] = True
    messages = []
    counter = 0
    for i in message_list:
        if counter >= start and counter <= length:
            messages.insert(0, i)   
        counter += 1

    details = {
        'messages':messages,
        'start': start,
        'end': end
    }
    
    return details

def channel_invite(token, channel_id, u_id):
    #Input Checking
    if decode_token(token) == False:
        raise AccessError(description ='Token is invalid')
    if isinstance(channel_id, int) == False:
        raise InputError(description ='Channel ID is not a valid channel')
    if channel_id >= dataFile.num_channels or channel_id < 0:
        raise InputError(description ='Channel ID is not a valid channel')
    if isinstance(u_id, int) == False:
        raise InputError(description ='User ID is not a valid user')
    if u_id >= dataFile.num_users or u_id < 0:
        raise InputError(description ='User ID is not a valid user')
    
    auth_user = decode_token(token)['u_id']
    owner_list = dataFile.data['channels'][channel_id]['owners']
    member_list = dataFile.data['channels'][channel_id]['members']
    
    if member_list.count(auth_user) == 0:
        raise AccessError(description ='Authorised user is not already a member of the channel')
    
    if member_list.count(u_id) > 0: 
        return {}
    
    member_list.append(u_id)
    
    #Global owner with permissions in every channel
    if dataFile.data['users'][u_id]['permission_id'] == 1:
        owner_list.append(u_id)
    
    return {}
    

def channel_leave(token, channel_id):
    #Input Checking
    if decode_token(token) == False:
        raise AccessError(description ='Token is invalid')
    if isinstance(channel_id, int) == False:
        raise InputError(description ='Channel ID is not a valid channel')
    if channel_id >= dataFile.num_channels or channel_id < 0:
        raise InputError(description ='Channel ID is not a valid channel')
   
    #Carrying out the function task
    owner_list = dataFile.data['channels'][channel_id]['owners']
    member_list = dataFile.data['channels'][channel_id]['members']
    
    u_id = decode_token(token)['u_id']
    
    if member_list.count(u_id) == 0:
        raise AccessError(description = 'Authorised user is not a member of channel with channel_id')
    
    if owner_list.count(u_id) > 0: 
        owner_list.remove(u_id)
    
    member_list.remove(u_id)
   
    return {
    }

def channel_join(token, channel_id): 
    #Input Checking
    if decode_token(token) == False:
        raise AccessError(description ='Token is invalid')
    if isinstance(channel_id, int) == False:
        raise InputError(description ='Channel ID is not a valid channel')
    if channel_id >= dataFile.num_channels or channel_id < 0:
        raise InputError(description ='Channel ID is not a valid channel')
    
    #Carrying out the function task
    u_id = decode_token(token)['u_id']
    owner_list = dataFile.data['channels'][channel_id]['owners']
    member_list = dataFile.data['channels'][channel_id]['members']
    
    if dataFile.data['users'][u_id]['permission_id'] == 2 and dataFile.data['channels'][channel_id]['is_public'] == False:
        raise AccessError(description ='Channel ID refers to a channel that is private')
    
    #Channel ID refers to a channel that authorised user has already joined
    if member_list.count(u_id) > 0: 
        return {}
    
    member_list.append(u_id)
    
    #Very first user is the owner of slackr with permissions in every channel
    if dataFile.data['users'][u_id]['permission_id'] == 1:
        owner_list.append(u_id) 
    
    return {}

def channel_addowner(token, channel_id, u_id): 
    #Input Checking
    if decode_token(token) == False:
        raise AccessError(description ='Token is invalid')
    if isinstance(channel_id, int) == False:
        raise InputError(description ='Channel ID is not a valid channel')
    if channel_id >= dataFile.num_channels or channel_id < 0:
        raise InputError(description ='Channel ID is not a valid channel')
    
    owner_list = dataFile.data['channels'][channel_id]['owners']
    member_list = dataFile.data['channels'][channel_id]['members']
    auth_user = decode_token(token)['u_id']
    
    if owner_list.count(u_id) > 0:
        raise InputError(description ='User ID is already an owner of the channel') 
    if member_list.count(u_id) == 0:
        return {}
    
    #AccessErrorHTTP Test
    if owner_list.count(auth_user) == 0 and auth_user > 0:
        raise AccessError(description ='Authorised user is not an owner of this channel or flockr')
    
    #Carrying out the function task
    owner_list.append(u_id)
    
    return {}

def channel_removeowner(token, channel_id, u_id):
    #Input Checking 
    if decode_token(token) == False:
        raise AccessError(description ='Token is invalid')
    if isinstance(channel_id, int) == False:
        raise InputError(description ='Channel ID is not a valid channel')
    if channel_id >= dataFile.num_channels or channel_id < 0:
        raise InputError(description ='Channel ID is not a valid channel')
    
    owner_list = dataFile.data['channels'][channel_id]['owners']
    auth_user = decode_token(token)['u_id']
    
    if owner_list.count(u_id) == 0:
        raise InputError(description ='User ID is not an owner of the channel')
    if dataFile.data['users'][u_id]['permission_id'] == 1:
        return {}
        
    #AccessErrorHTTP Test
    if owner_list.count(auth_user) == 0 and auth_user > 0:
        raise AccessError(description ='Authorised user is not an owner of this channel or flockr')
    
    #Carrying out the function task
    owner_list.remove(u_id)
    
    return {}