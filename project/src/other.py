import dataFile
#from json import dumps
#from flask import Flask, request
from error import InputError, AccessError
from help_functions import decode_token

def clear():
    dataFile.num_users = 0
    dataFile.num_channels = 0
    user = dataFile.data['users']
    user.clear()
    channels = dataFile.data['channels']
    channels.clear()
    return {}

def users_all(token):
    if decode_token(token) == False:
        raise AccessError(description ='Token is invalid')
    return {
        'users': dataFile.data['users'],
    }

def admin_userpermission_change(token, u_id, permission_id):
    if decode_token(token) == False:
        raise AccessError(description ='Token is invalid')
    if isinstance(u_id, int) == False:
        raise InputError(description ='User ID is not a valid user')
    if u_id >= dataFile.num_users or u_id < 0:
        raise InputError(description ='User ID is not a valid user')
    if permission_id != 1 and permission_id != 2:
        raise InputError(description ='Permission_ID is not valid')
    
    auth_user = decode_token(token)['u_id']
    if dataFile.data['users'][auth_user]['permission_id'] != 1:
        raise AccessError(description='The authorised user is not an owner')

    dataFile.data['users'][u_id]['permission_id'] = permission_id
    return {}

def search(token, query_str):
    if decode_token(token) == False:
        raise AccessError(description ='Token is invalid')
    auth_user = decode_token(token)['u_id']
    result = {
        'messages':[],
    }
    for channel in dataFile.data['channels']:
        if channel['members'].count(auth_user) > 0:     
            for string in channel['messages']:
                if auth_user == string['u_id'] and query_str in string['message']:
                    result['messages'].append(string)
    return result

