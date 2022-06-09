import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests
import json
from help_functions import generate_token
from requests.exceptions import HTTPError

@pytest.fixture
def url():
    url_re = re.compile(r' \* Running on ([^ ]*)')
    server = Popen(["python3", "src/server.py"], stderr=PIPE, stdout=PIPE)
    line = server.stderr.readline()
    local_url = url_re.match(line.decode())
    if local_url:
        yield local_url.group(1)
        # Terminate the server
        server.send_signal(signal.SIGINT)
        waited = 0
        while server.poll() is None and waited < 5:
            sleep(0.1)
            waited += 0.1
        if server.poll() is None:
            server.kill()
    else:
        server.kill()
        raise Exception("Couldn't get URL from local server")


def test_active_token_error(url):
    requests.delete(url + "clear")
    # get a valid token to get a channel
    param0 = {'email': "test@gmail.com", 'password': "easypass",
              'name_first': "Nick", 'name_last': "Sal"}
    x = requests.post(url + 'auth/register', json=param0)
    token = x.json()['token']
    param1 = {'token': token, 'name': 'team1', 'is_public': False}
    # create a new channel to make sure the channel_id is true
    x = requests.post(url + 'channels/create', json=param1)
    channel_id = x.json()['channel_id']
    param2 = {"token": 'incorrect1', "channel_id": channel_id}
    p = requests.get(url + '/standup/active', params=param2)
    assert p.json()['code'] == 400

def test_active_channelId_error(url):
    requests.delete(f"{url}/clear")
    # get a correct token
    param0 = {'email': "test@gmail.com", 'password': "easypass",
              'name_first': "Nick", 'name_last': "Sal"}
    x = requests.post(url + 'auth/register', json=param0)
    token = x.json()['token']
    # incorrect channel_id
    param1 = {"token": token, "channel_id": 45646}
    p = requests.get(url + '/standup/active', params=param1)
    assert p.json()['code'] == 400

def test_start_twice_active_error(url):
    requests.delete(f"{url}/clear")
    # get a valid token to get a channel
    param0 = {'email': "test@gmail.com", 'password': "easypass",
              'name_first': "Nick", 'name_last': "Sal"}
    x = requests.post(url + 'auth/register', json=param0)
    token = x.json()['token']
    param1 = {'token': token, 'name': 'team1', 'is_public': False}
    # create a new channel to make sure the channel_id is true
    x = requests.post(url + 'channels/create', json=param1)
    channel_id = x.json()['channel_id']
    param2 = {"token": token, "channel_id": channel_id, 'length': 10}
    requests.post(url + '/standup/start', json=param2)
    # active twice
    p = requests.post(url + '/standup/start', json=param2)
    assert p.json()['code'] == 400
'''
def test_start_token_error(url):
    requests.delete(url + "clear")
    # get a valid token to get a channel
    param0 = {'email': "test@gmail.com", 'password': "easypass",
              'name_first': "Nick", 'name_last': "Sal"}
    x = requests.post(url + 'auth/register', json=param0)
    token = x.json()['token']
    param1 = {'token': token, 'name': 'team1', 'is_public': False}
    # create a new channel to make sure the channel_id is true
    x = requests.post(url + 'channels/create', json=param1)
    channel_id = x.json()['channel_id']
    param2 = {"token": 'incorrect1', "channel_id": channel_id}
    p = requests.post(url + '/standup/start', json=param2)
    assert p.json()['code'] == 400

def test_start_channelId_error(url):
    requests.delete(f"{url}/clear")
    # get a correct token
    param0 = {'email': "test@gmail.com", 'password': "easypass",
              'name_first': "Nick", 'name_last': "Sal"}
    x = requests.post(url + 'auth/register', json=param0)
    token = x.json()['token']
    # incorrect channel_id
    param1 = {"token": token, "channel_id": 45646}
    p = requests.post(url + '/standup/start', json=param1)
    assert p.json()['code'] == 400

def test_start_channelId_int_error(url):
    requests.delete(f"{url}/clear")
    # get a correct token
    param0 = {'email': "test@gmail.com", 'password': "easypass",
              'name_first': "Nick", 'name_last': "Sal"}
    x = requests.post(url + 'auth/register', json=param0)
    token = x.json()['token']
    # incorrect channel_id
    param1 = {"token": token, "channel_id": 2.15345}
    p = requests.post(url + '/standup/start', json=param1)
    assert p.json()['code'] == 400
'''
def test_send_message_error(url):
    requests.delete(f"{url}/clear")
    # get a valid token to get a channel
    param0 = {'email': "test@gmail.com", 'password': "easypass",
              'name_first': "Nick", 'name_last': "Sal"}
    x = requests.post(url + 'auth/register', json=param0)
    token = x.json()['token']
    # create a list contains more than 1000 character
    message = ""
    i = 0
    while i <= 1000:
        message += 'aaaa'
        i += 1
    param1 = {'token': token, 'name': 'team1', 'is_public': False}
    # create a new channel to make sure the channel_id is true
    x = requests.post(url + 'channels/create', json=param1)
    channel_id = x.json()['channel_id']
    # start the standup
    correct_param = {'token': token, 'channel_id': channel_id, 'length': 10}
    requests.post(url + '/standup/start', json=correct_param)
    param2 = {'token': token, 'channel_id': channel_id, 'message': message}
    p = requests.post(url + '/standup/send', json=param2)
    assert p.json()['code'] == 400
'''
def test_send_token_error(url):
    requests.delete(url + "clear")
    # get a valid token to get a channel
    param0 = {'email': "test@gmail.com", 'password': "easypass",
              'name_first': "Nick", 'name_last': "Sal"}
    x = requests.post(url + 'auth/register', json=param0)
    token = x.json()['token']
    param1 = {'token': token, 'name': 'team1', 'is_public': False}
    channel_id = requests.post(url + 'channels/create', json=param1)
    # active the standup
    correct_param = {'token': token, 'channel_id': channel_id, 'length': 10}
    requests.post(url + '/standup/start', json=correct_param)
    param2 = {"token": 'incorrect1', "channel_id": channel_id,
              'message': 'kevin so handsome'}
    p = requests.post(url + '/standup/send', json=param2)
    assert p.json()['code'] == 400

def test_send_channelId_error(url):
    requests.delete(f"{url}/clear")
    # get a correct token
    param0 = {'email': "test@gmail.com", 'password': "easypass",
              'name_first': "Nick", 'name_last': "Sal"}
    x = requests.post(url + 'auth/register', json=param0)
    token = x.json()['token']
    param1 = {'token': token, 'name': 'team1', 'is_public': False}
    channel_id = requests.post(url + 'channels/create', json=param1)
    # active the standup
    correct_param = {'token': token, 'channel_id': channel_id, 'length': 10}
    requests.post(url + '/standup/start', json=correct_param)
    channel_id = x.json()['channel_id']
    # incorrect channel_id
    param1 = {"token": token, "channel_id": 45646,
              'message': 'kevin so handsome'}
    p = requests.post(url + '/standup/send', json=param1)
    assert p.json()['code'] == 400

def test_send_channelId_int_error(url):
    requests.delete(f"{url}/clear")
    # get a correct token
    param0 = {'email': "test@gmail.com", 'password': "easypass",
              'name_first': "Nick", 'name_last': "Sal"}
    x = requests.post(url + 'auth/register', json=param0)
    token = x.json()['token']
    param1 = {'token': token, 'name': 'team1', 'is_public': False}
    channel_id = requests.post(url + 'channels/create', json=param1)
    # active the standup
    correct_param = {'token': token, 'channel_id': channel_id, 'length': 10}
    requests.post(url + '/standup/start', json=correct_param)
    # test not active
    channel_id = x.json()['channel_id']
    # incorrect channel_id
    param2 = {"token": token, "channel_id": 2.476285386,
              'message': 'kevin so handsome'}
    p = requests.post(url + '/standup/send', json=param2)
    assert p.json()['code'] == 400

def test_send_active_error(url):
    requests.delete(f"{url}/clear")
    # get a valid token to get a channel
    param0 = {'email': "test@gmail.com", 'password': "easypass",
              'name_first': "Nick", 'name_last': "Sal"}
    x = requests.post(url + 'auth/register', json=param0)
    token = x.json()['token']
    param1 = {'token': token, 'name': 'team1', 'is_public': False}
    # create a new channel to make sure the channel_id is true
    channel_id = requests.post(url + 'channels/create', json=param1)
    # test not active
    channel_id = x.json()['channel_id']
    param2 = {"token": token, "channel_id": channel_id,
              'message': 'kevin so handsome'}
    p = requests.post(url + '/standup/send', json=param2)
    assert p.json()['code'] == 400

def test_send_user_error(url):
    requests.delete(f"{url}/clear")
    # get a valid token to get a channel
    param0 = {'email': "test@gmail.com", 'password': "easypass",
              'name_first': "Nick", 'name_last': "Sal"}
    x = requests.post(url + 'auth/register', json=param0)
    token1 = x.json()['token']
    # get a valid token to get a channel
    param1 = {'email': "test1@gmail.com", 'password': "easyyypass",
              'name_first': "Nickkk", 'name_last': "Sallll"}
    x = requests.post(url + 'auth/register', json=param1)
    token2 = x.json()['token']
    param2 = {'token': token1, 'name': 'team1', 'is_public': False}
    # create a new channel to make sure the channel_id is true
    channel_id = requests.post(url + 'channels/create', json=param2)
    correct_param = {'token': token1, 'channel_id': channel_id}
    requests.post(url + 'standup/active', json=correct_param)
    param3 = {"token": token2, "channel_id": channel_id,
              'message': 'kevin so handsome'}
    p = requests.post(url + '/standup/send', json=param3)
    assert p.json()['code'] == 400
'''