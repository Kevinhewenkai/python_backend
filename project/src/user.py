import dataFile
from error import InputError, AccessError
from help_functions import decode_token, check

def user_profile(token, u_id):
    #error checking
    if decode_token(token) == False:
        raise AccessError(description ='Token is invalid')
    if isinstance(u_id, int) == False:
        raise InputError(description ='User with u_id is not a valid user')
    if isinstance(token, str) == False:
        raise InputError(description ='Token is not valid')
    if u_id >= dataFile.num_users or u_id < 0:
        raise InputError(description ='User ID is not a valid user')

    email = dataFile.data['users'][u_id]['email']
    first = dataFile.data['users'][u_id]['name_first']
    last = dataFile.data['users'][u_id]['name_last']
    handle = dataFile.data['users'][u_id]['handle']

    user_info = {
        'u_id': u_id, 
        'email': email, 
        'name_first': first, 
        'name_last': last,
        'handle_str': handle,
        'profile_img_url': dataFile.data['users'][u_id]['profile_img_url']
    }

    result = {
        'user': user_info
    }

    return (result)

def user_profile_setname(token, name_first, name_last):
    fn_len = len(name_first)
    ln_len = len(name_last)

    #error checking
    if decode_token(token) == False:
        raise AccessError(description ='Token is invalid')
    if fn_len < 1 or fn_len > 50:
        raise InputError(description ='First name is not between 1 and 50 characters')
    if ln_len < 1 or ln_len > 50:
        raise InputError(description ='Last name is not between 1 and 50 characters')

    #if valid and matching token find uid
    u_id = decode_token(token)['u_id']
    for dictionary in dataFile.data['users']:
        if dictionary['u_id'] == u_id:
            dictionary['name_first'] = name_first
            dictionary['name_last'] = name_last

    return ({})

def user_profile_setemail(token, email):
    if decode_token(token) == False:
        raise AccessError(description ='Token is invalid')
    #Input error checking
    if check(email) == False:
        raise InputError(description ='Not a valid email')

    for dictionary in dataFile.data['users']:
        if email == dictionary['email']:
            raise InputError(description ='Email address is already being used by another user')

    #find the user by using token
    u_id = decode_token(token)['u_id']
    for user_detail in dataFile.data['users']:
        if u_id == user_detail['u_id']:
            user_detail['email'] = email

    return ({})

def user_profile_sethandle(token, handle_str):
    if decode_token(token) == False:
        raise AccessError(description ='Token is invalid')

    if len(handle_str) < 3 or len(handle_str) > 20:
        raise InputError("handle_str must be between 3 and 20 characters")

    for handles in dataFile.data['users']:
        if handle_str == handles['handle']:
            raise InputError(description ='handle is already used by another user')

    #find the user by using token
    u_id = decode_token(token)['u_id']
    for user_detail in dataFile.data["users"]:
        if u_id == user_detail["u_id"]:
            user_detail["handle"] = handle_str

    return ({})