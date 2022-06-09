import sys
import time
import dataFile
import urllib.request
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from PIL import Image
from error import InputError, AccessError
from auth import auth_register, auth_login, auth_logout, auth_passwordreset_request, auth_passwordreset_reset
from channel import channel_details, channel_messages, channel_invite, channel_join, channel_leave, channel_addowner, channel_removeowner
from user import user_profile, user_profile_sethandle, user_profile_setemail, user_profile_setname
from message import message_send, message_remove, message_edit, message_sendlater, message_react, message_unreact, message_pin, message_unpin
from standup import standup_active, standup_send, standup_start
from other import clear, users_all, admin_userpermission_change, search
from channels import channels_list, channels_listall, channels_create
from help_functions import decode_token, check, generate_token, message_future, end_standup

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
        raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

##############################################################
######################## AUTH ################################

@APP.route("/auth/login", methods=['POST'])
def auth_login_http():
    payload = request.get_json()
    email = payload['email']
    password = payload['password']
    return dumps(auth_login(email, password))

@APP.route("/auth/logout", methods=['POST'])
def auth_logout_http():
    payload = request.get_json()
    token = payload['token']
    return dumps(auth_logout(token))

@APP.route("/auth/register", methods=['POST'])
def auth_register_http():
    payload = request.get_json()
    email = payload['email']
    password = payload['password']
    name_first = payload['name_first']
    name_last = payload['name_last']
    return dumps(auth_register(email, password, name_first, name_last))

@APP.route("/auth/passwordreset/request", methods=['POST'])
def auth_passwordreset_request_http():
    payload = request.get_json()
    email = payload['email']
    return dumps(auth_passwordreset_request(email))

@APP.route("/auth/passwordreset/reset", methods=['POST'])
def auth_passwordreset_reset_http():
    payload = request.get_json()
    reset_code = payload['reset_code']
    new_password = payload['new_password']
    return dumps(auth_passwordreset_reset(reset_code, new_password))

##############################################################
######################## CHANNEL #############################

@APP.route("/channel/details", methods=['GET'])
def channel_details_http():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    return dumps(channel_details(token, channel_id))

@APP.route("/channel/messages", methods=['GET'])
def channel_messages_http():
    token = request.args.get('token')
    start = int(request.args.get('start'))
    channel_id = int(request.args.get('channel_id'))
    return dumps(channel_messages(token, channel_id, start))

@APP.route("/channel/invite", methods=['POST'])
def channel_invite_http():
    payload = request.get_json()
    token = payload['token']
    u_id = int(payload['u_id'])
    channel_id = int(payload['channel_id'])
    return dumps(channel_invite(token, channel_id, u_id))

@APP.route("/channel/leave", methods=['POST'])
def channel_leave_http():
    payload = request.get_json()
    token = payload['token']
    channel_id = int(payload['channel_id'])
    return dumps(channel_leave(token, channel_id))

@APP.route("/channel/join", methods=['POST'])
def channel_join_http():
    payload = request.get_json()
    token = payload['token']
    channel_id = int(payload['channel_id'])
    return dumps(channel_join(token, channel_id))

@APP.route("/channel/addowner", methods=['POST'])
def channel_addowner_http():
    payload = request.get_json()
    token = payload['token']
    u_id = int(payload['u_id'])
    channel_id = int(payload['channel_id'])
    return dumps(channel_addowner(token, channel_id, u_id))

@APP.route("/channel/removeowner", methods=['POST'])
def channel_removeowner_http():
    payload = request.get_json()
    token = payload['token']
    u_id = int(payload['u_id'])
    channel_id = int(payload['channel_id'])
    return dumps(channel_removeowner(token, channel_id, u_id))

##############################################################
######################## CHANNELS ############################

@APP.route('/channels/list', methods=['GET'])
def channels_list_http():
    token = request.args.get('token')
    return dumps(channels_list(token))

@APP.route('/channels/listall', methods=['GET'])
def channels_listall_http():
    token = request.args.get('token')
    return dumps(channels_listall(token))

@APP.route('/channels/create', methods=['POST'])
def channels_create_http():
    payload = request.get_json()
    token = payload['token']
    name = payload['name']
    is_public = payload['is_public']
    return dumps(channels_create(token, name, is_public))

##############################################################
######################## USER ################################

@APP.route("/user/profile", methods=['GET'])
def user_profile_http():
    token = request.args.get('token')
    u_id = int(request.args.get('u_id'))
    return dumps(user_profile(token, u_id))

@APP.route("/user/profile/setemail", methods=['PUT'])
def user_profile_setemail_http():
    payload = request.get_json()
    token = payload['token']
    email = payload['email']
    return dumps(user_profile_setemail(token, email))

@APP.route("/user/profile/setname", methods=['PUT'])
def user_profile_setname_http():
    payload = request.get_json()
    token = payload['token']
    name_first = payload['name_first']
    name_last = payload['name_last']
    return dumps(user_profile_setname(token, name_first, name_last))

@APP.route("/user/profile/sethandle", methods=['PUT'])
def user_profile_sethandle_http():
    payload = request.get_json()
    token = payload['token']
    handle_str = payload['handle_str']
    return dumps(user_profile_sethandle(token, handle_str))

##############################################################
######################## MESSAGES ############################

@APP.route("/message/send", methods=['POST'])
def message_send_http():
    payload = request.get_json()
    token = payload['token']
    channel_id = int(payload['channel_id'])
    message = payload['message']
    return dumps(message_send(token, channel_id, message))

@APP.route("/message/remove", methods=['DELETE'])
def message_remove_http():
    payload = request.get_json()
    token = payload['token']
    message_id = int(payload['message_id'])
    return dumps(message_remove(token, message_id))

@APP.route("/message/edit", methods=['PUT'])
def message_edit_http():
    payload = request.get_json()
    token = payload['token']
    message_id = int(payload['message_id'])
    message = payload['message']
    return dumps(message_edit(token, message_id, message))

@APP.route("/message/sendlater", methods=['POST'])
def message_sendlater_http():
    payload = request.get_json()
    token = payload['token']
    channel_id = int(payload['channel_id'])
    message = payload['message']
    time_sent = payload['time_sent']
    return dumps(message_sendlater(token, channel_id, message, time_sent))

@APP.route("/message/react", methods=['POST'])
def message_react_http():
    payload = request.get_json()
    token = payload['token']
    message_id = int(payload['message_id'])
    react_id = payload['react_id']
    return dumps(message_react(token, message_id, react_id))

@APP.route("/message/unreact", methods=['POST'])
def message_unreact_http():
    payload = request.get_json()
    token = payload['token']
    message_id = int(payload['message_id'])
    react_id = payload['react_id']
    return dumps(message_unreact(token, message_id, react_id))

@APP.route("/message/pin", methods=['POST'])
def message_pin_http():
    payload = request.get_json()
    token = payload['token']
    message_id = int(payload['message_id'])
    return dumps(message_pin(token, message_id))

@APP.route("/message/unpin", methods=['POST'])
def message_unpin_http():
    payload = request.get_json()
    token = payload['token']
    message_id = int(payload['message_id'])
    return dumps(message_unpin(token, message_id))

##############################################################
######################## STANDUP #############################

@APP.route("/standup/active", methods=['GET'])
def standup_active_http():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    return dumps(standup_active(token, channel_id))

@APP.route("/standup/start", methods=['POST'])
def standup_start_http():
    payload = request.get_json()
    token = payload['token']
    channel_id = int(payload['channel_id'])
    length = int(payload['length'])
    return dumps(standup_start(token, channel_id, length))

@APP.route("/standup/send", methods=['POST'])
def standup_send_http():
    payload = request.get_json()
    token = payload['token']
    channel_id = int(payload['channel_id'])
    message = payload['message']
    return dumps(standup_send(token, channel_id, message))

##############################################################
######################## OTHER ###############################

@APP.route("/clear", methods=['DELETE'])
def clear_http():
    return dumps(clear())

@APP.route("/users/all", methods=['GET'])
def users_all_http():
    token = request.args.get('token')
    return dumps(users_all(token))

@APP.route("/admin/userpermission/change", methods=['POST'])
def admin_userpermission_change_http():
    payload = request.get_json()
    token = payload['token']
    u_id = payload['u_id']
    permission_id = payload['permission_id']
    return dumps(admin_userpermission_change(token, u_id, permission_id))

@APP.route("/search", methods=['GET'])
def search_http():
    token = request.args.get('token')
    query_str = request.args.get('query_str')
    return dumps(search(token, query_str))

@APP.route('/user/profile/uploadphoto', methods=['POST'])
def user_profile_uploadphoto():
    payload = request.get_json()
    token = payload['token']
    img_url = payload['img_url']
    x_start = int(payload['x_start'])
    y_start = int(payload['y_start'])
    x_end = int(payload['x_end'])
    y_end = int(payload['y_end'])

    urllib.request.urlretrieve(img_url, './src/static/example.jpg')
    ImageObject = Image.open('./src/static/example.jpg')

    x_max, y_max = ImageObject.size

    if x_start < 0 or y_start < 0 or x_end > x_max or y_end > y_max or x_start > x_end or y_start > y_end:
        raise InputError(description ='cropping size is wrong')

    cropped = ImageObject.crop((x_start, y_start, x_end, y_end))
    cropped.save('./src/static/example.jpg')

    u_id = decode_token(token)['u_id']

    for dictionary in dataFile.data['users']:
        if u_id == dictionary['u_id']:
            #dictionary['profile_img_url'] = test
            dictionary['profile_img_url'] = './src/example.jpg'
    return dumps({})

if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port
