import jwt
import re
import base64
import dataFile
import time
import random
import string
import smtplib
from error import AccessError, InputError

SECRET = "ABCACHBDABFGJASDdfbajfdbdjsfbCXAXZ<CVN"

def check(email):
    if re.search(r'[\w.-]+@[\w.-]+', email):
        return True
    else:
        return False

def generate_token(u_id):
    encoded_jwt = jwt.encode({"u_id": u_id}, SECRET, algorithm='HS256').decode("utf-8")
    #print(encoded_jwt)
    return encoded_jwt

def decode_token(token):
    try:
        u_id = jwt.decode(token, SECRET, algorithms=['HS256'])
        return u_id
    except jwt.exceptions.DecodeError:
        return False

def encrypt(password):
    encodedpassword = base64.b64encode(password.encode("utf-8"))
    return encodedpassword

def decrypt(encodedpassword):
    password = base64.b64decode(encodedpassword).decode("utf-8")
    return password

def message_future(token, channel_id, message):
    message_list = dataFile.data['channels'][channel_id]['messages']
    u_id = decode_token(token)['u_id']
    now = int(time.time())
    detail = {
        'message_id': dataFile.num_messages_created,
        'u_id': u_id,
        'message': message,
        'time_created': now,
    }
    dataFile.data['channels'][channel_id]['total_messages'] += 1
    message_list.append(detail)
 
def end_standup(token, channel_id):
    dataFile.data['channels'][channel_id]['is_standup_active'] = False
    message = dataFile.data['channels'][channel_id]['standup_queue']
    message_standup(token, channel_id, message)
    dataFile.data['channels'][channel_id]['standup_queue'] = ''

def message_standup(token, channel_id, message):
    message_list = dataFile.data['channels'][channel_id]['messages']
    u_id = decode_token(token)['u_id']
    now = int(time.time())
    dataFile.num_messages_created += 1
    detail = {
        'message_id': dataFile.num_messages_created,
        'u_id': u_id,
        'message': message,
        'time_created': now,
    }
    dataFile.data['channels'][channel_id]['total_messages'] += 1
    message_list.append(detail)

def get_random_code(size=50, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def send_email(email, reset_code):
    subject = "f11orangeteam1's flockr password reset code"
    server=smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login('grouponeorange@gmail.com', 'orange123!')
    message = 'Subject: {}\n\n{}'.format(subject, reset_code)
    server.sendmail('grouponeorange@gmail.com', email, message)
    server.quit()

def message_find(message_id, u_id, permission):
    for channel in dataFile.data['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                if permission == 2 and channel['owners'].count(u_id) == 0:
                    raise AccessError('Message was not sent by authorised user and and there is no owner status')
                return message
    return {}

def message_find_react(message_id, u_id, permission, react_id):
    for channel in dataFile.data['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                if channel['members'].count(u_id) == 0:
                    raise InputError('message_id is not a valid message within a channel that the authorised user has joined')
                return message
    return {}

def pin(message, pinning):
    if message == {}:
        raise InputError('message_id is not a valid message ID')
    if message['is_pinned'] is not pinning:
        message['is_pinned'] = pinning
    else:
        raise InputError("Message with ID message_id is already pinned or unpinned") #CHANGE THIS TO RETURN {} LATER
    return {}

def reacts(message, react_id):
    if message == {}:
        raise InputError('message_id is not a valid message ID')
    for react in message['reacts']:
        if react['react_id'] == react_id:
            return react
    return False

