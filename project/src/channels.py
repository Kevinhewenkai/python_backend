'''
channels contains function channels_list, channels_listall, channels_create
'''
'''
from json import dumps
from flask import Flask, request
'''
from error import InputError, AccessError
from help_functions import decode_token
import dataFile
# app = Flask(__name__)

# @app.route('channels/list', method=['GET'])
def channels_list(token):
    '''
    Provide a list of all channels (and their associated details) that
    the authorised user is part of
    '''
    if decode_token(token) == False:
        raise AccessError(description ='Token is invalid')

    user_part_of_list = []
    u_id = decode_token(token)['u_id']

    # find the dictionary of channels
    # channel_details is a dictionary
    for channel_details in dataFile.data['channels']:
        # find the u_id of member in a list
        # menber_id is a list with u_id in it
        for member_id in channel_details['members']:
            if u_id == member_id:
                user_part_of_list.append(channel_details)

    user_list = {
        'channels': user_part_of_list
    }

    return (user_list)

# @app.route('channels/listall', method=['GET'])
def channels_listall(token):
    '''
    Provide a list of all channels (and their associated details)
    '''
    # check whether the token is valid
    if decode_token(token) == False:
        raise AccessError(description ='Token is invalid')
    channel_list = {
        'channels': dataFile.data['channels']
    }
    return (channel_list)

# @app.route('channels/create', method=['POST'])
def channels_create(token, name, is_public):
    '''
    Creates a new channel with that name that is either a public or private channel
    '''
    if decode_token(token) == False:
        raise AccessError(description ='Token is invalid')

    u_id = decode_token(token)['u_id']
    if len(name) > 20:
        raise InputError(description ="Name is more than 20 characters long")

    # class of a channel
    new_channel = {
        'channel_id': dataFile.num_channels,
        'name' : name,
        'owners': [u_id],
        'members': [u_id],
        'total_messages': 0,
        'messages': [],
        'is_public' : is_public,
        'is_standup_active': False,
        'time_finish': 0,
        'standup_queue' : '',
    }
    dataFile.data['channels'].append(new_channel)
    dataFile.num_channels += 1
    
    return ({
        'channel_id': dataFile.num_channels - 1,
    })
