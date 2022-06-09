import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep, time
import requests



# Use this fixture to get the URL of the server. It starts the server for you,
# so you don't need to.
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

def test_message_sendlater_exc(url):
    #Preparing tests
    requests.delete(url + 'clear')
    resp = requests.post(url + 'auth/register', json = {'email': 'test@gmail.com', 'password': 'password123', 'name_first': 'Vince', 'name_last': 'Lam'})
    t1 = resp.json()['token']
    name = "team1"
    is_public = True
    param = {'token' : t1, 'name' : name, 'is_public' : is_public}
    payload = requests.post(url + 'channels/create', json = param)
    channel_id = payload.json()['channel_id']

    #Checking for AccessErrorHTTP (Invalid Token)
    param = {'token' : 999, 'channel_id' : channel_id, 'message' : 'hello', 'time_sent': time()}
    resp = requests.post(url + 'message/sendlater', json = param)
    assert resp.json()['code'] == 400
    
    #Checking for InputErrorHTTP (Invalid Channel ID)
    channel_id += 1
    param = {'token' : t1, 'channel_id' : channel_id, 'message' : 'hello', 'time_sent': time()}
    resp = requests.post(url + 'message/sendlater', json = param)
    assert resp.json()['code'] == 400

    #Checking for InputErrorHTTP (Time sent is in the past)
    channel_id -= 1
    past = time() - 1
    i = 0
    long_message = ''
    while i <= 1000:
        long_message += 'a'
        i += 1

    param = {'token' : t1, 'channel_id' : channel_id, 'message' : 'hello', 'time_sent': past}
    resp = requests.post(url + 'message/sendlater', json = param)
    assert resp.json()['code'] == 400

    #Checking for InputErrorHTTP (Message > 1000 chars)
    param = {'token' : t1, 'channel_id' : channel_id, 'message' : long_message, 'time_sent': time()}
    resp = requests.post(url + 'message/sendlater', json = param)
    assert resp.json()['code'] == 400

def test_http_messages_edit_assessing_1(url):
    requests.delete(url + 'clear')

    x = requests.post(url + 'auth/register', json = {'email' : "test@gmail.com", 
              'password' : "easypass", 
              'name_first' : "Nick", 
              'name_last' : "Sal"
    })
    token1 = x.json()['token']

    x = requests.post(url + 'auth/register', json = {'email' : "test1@gmail.com", 
              'password' : "easypass", 
              'name_first' : "Nick", 
              'name_last' : "Sal"
    })
    token2 = x.json()['token']

    x = requests.post(url + 'channels/create', json = {
        'token' : token1, 
        'name' : 'team1', 
        'is_public' : False,
    })
    channel_id_1 = x.json()['channel_id']

    requests.post(url + 'channels/join', json = {
        'token' : token2, 
        'channel_id' : channel_id_1,
    })

    message1 = 'Sup'
    message_id_1 = requests.post(url + 'message/send', json = {
        'token': token1,
        'channel_id': channel_id_1,
        'message': message1,
    }).json()['message_id']

    requests.post(url + 'channels/leave', json = {
        'token' : token2,
        'channel_id' : channel_id_1,
    })

    p = requests.put(url + 'message/edit', json = {
        'token': token2,
        'message_id': message_id_1,
        'message': 'Sup',
    })
    assert p.json()['code'] == 400

def test_channel_detail_assessing_1(url):
    #Create channel
    requests.delete(url + 'clear')
    
    x = requests.post(url + 'auth/register', json = {
        'email' : "test@gmail.com", 
        'password' : "easypass", 
        'name_first' : "Nick", 
        'name_last' : "Sal"
    })
    token1 = x.json()['token']

    x = requests.post(url + 'channels/create', json = {
        'token' : token1, 
        'name' : 'team1', 
        'is_public' : False,
    })
    channel_id = x.json()['channel_id']
    
    #User is trying to detail the channel without being apart of it
    #This is a access error
    x = requests.post(url + 'auth/register', json = {
        'email' : "testasdasd1@gmail.com", 
        'password' : "easypass", 
        'name_first' : "Nick", 
        'name_last' : "Sal"
    })
    token2 = x.json()['token']

    # channel_details(token2,channel_id)
    
    p = requests.get(url + 'channel/details', params = {
            'token': token2,
            'channel_id': channel_id,
    })

    assert p.json()['code'] == 400
