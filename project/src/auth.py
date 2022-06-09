import dataFile
from error import InputError, AccessError
from help_functions import generate_token, decode_token, check, encrypt, decrypt, get_random_code, send_email

def auth_login(email, password):
    #Input error checking
    if check(email) == False:
        raise InputError(description ='Not a valid email')

    #checker to see if found email
    token = "check"

    #loop through users and check if email and password are correct
    for dictionary in dataFile.data['users']:
        if email == dictionary['email']:
            if password == dictionary['password']:
                u_id = dictionary['u_id']
                token = generate_token(u_id)
                #dictionary['token'] = token
            else:
                raise InputError(description='Password is not correct')

    #check is token has been changed
    if token == 'check':
        raise InputError(description='Email entered does not belong to a user')

    return {
        'u_id': u_id,
        'token': token,
    }

def auth_logout(token):
    result = decode_token(token)
    if result == False:
        raise AccessError(description='Token is invalid')
    del token
    return {
        'is_success': True
    }

def auth_register(email, password, name_first, name_last):
    #length of strings that need checking
    pass_len = len(password)
    fn_len = len(name_first)
    ln_len = len(name_last)

    #Input error checking
    if check(email) == False:
        raise InputError(description='Not a valid email')
    for dictionary in dataFile.data['users']:
        if email == dictionary['email']:
            raise InputError(description ='Email address is already being used by another user')
    if pass_len < 6:
        raise InputError(description ='Password is too short')
    if fn_len < 1 or fn_len > 50:
        raise InputError(description ='First name is not between 1 and 50 characters')
    if ln_len < 1 or fn_len > 50:
        raise InputError(description ='Last name is not between 1 and 50 characters')

    #creating the handle
    combine_name = name_first + name_last
    handle = combine_name.lower()

    #create token and u_id
    u_id = dataFile.num_users
    token = generate_token(u_id)

    #determining permissions
    if dataFile.num_users == 0:
        permission_id = 1
    else:
        permission_id = 2

    #inserting dict into users
    new_user = {"u_id": u_id, "handle": handle, "email": email,
                "password": password, "name_first": name_first,
                "name_last": name_last, "permission_id": permission_id, "reset_code": '', 'profile_img_url':''}
    
    dataFile.data['users'].append(new_user)

    #increment uid counter
    dataFile.num_users += 1
    
    return {
        'u_id': u_id,
        'token': token,
    }

def auth_passwordreset_request(email):
    checker = 0
    #Input error checking
    if check(email) == False:
        raise InputError(description='Not a valid email')
    for dictionary in dataFile.data['users']:
        if email == dictionary ['email']:
            checker = 1

    if checker == 0:
        raise InputError(description='Not a valid email')

    reset_code = get_random_code()

    for dictionary in dataFile.data['users']:
        if email == dictionary ['email']:
            dictionary['reset_code'] = reset_code
    
    send_email(email, reset_code)
    return {
    }

def auth_passwordreset_reset(reset_code, new_password):
    pass_len = len(new_password)
    checker = 0
    if pass_len < 6:
        raise InputError("Password is too short")
    
    for dictionary in dataFile.data['users']:
        if reset_code == dictionary['reset_code']:
            dictionary['password'] = new_password
            dictionary['reset_code'] = ""
            checker = 1
    
    if checker == 0:
        raise InputError(description='not valid reset code')
    
    return {    
    }

