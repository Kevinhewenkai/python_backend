import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import json
import requests
from help_functions import generate_token


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

def test_channels_create(url):
    #clear()
    requests.delete(url + 'clear')
    #Create channel
    param1 = {'email' : "test@gmail.com", 'password' : "easypass", 'name_first' : "Nick", 'name_last' : "Sal"}
    x = requests.post(url + 'auth/register', json = param1)
    t1 = x.json()['token']
    name = "team1"
    is_public = True
    param1 = {'token' : t1, 'name' : name, 'is_public' : is_public}
 
    payload = requests.post(url + 'channels/create', json = param1)
    assert payload.json() == {'channel_id': 0}

# test the user is only in one channel
def test_channels_list(url):
    #clear()
    requests.delete(url + 'clear')
    #Empty return
    param1 = {'email' : "test@gmail.com", 'password' : "easypass", 'name_first' : "Nick", 'name_last' : "Sal"}
    x = requests.post(url + 'auth/register', json = param1)
    t1 = x.json()['token']
    #assert (channels_list(t1) == {'channels': []})
    assert requests.get(url + 'channels/list', params = {'token' : t1}).json() == {'channels': []}

def test_channels_listall(url):
    #clear()
    requests.delete(url + 'clear')
    #Empty return
    param1 = {'email' : "test@gmail.com", 'password' : "easypass", 'name_first' : "Nick", 'name_last' : "Sal"}
    x = requests.post(url + 'auth/register', json = param1)
    t1 = x.json()['token']
    resp = requests.get(url + 'channels/listall', params = {'token' : t1})
    assert resp.json() == {'channels': []}


def test_channels_create_exc(url):
    #clear()
    requests.delete(url + 'clear')
    param1 = {'email' : "test@gmail.com", 'password' : "easypass", 'name_first' : "Nick", 'name_last' : "Sal"}
    requests.post(url + 'auth/register', json = param1)
    #Invalid token test
    param1 = {
        'token' : 'incorrect1',
        'name' : 'team1',
        'is_public' : False,
    }

    #with pytest.raises(AccessError):
        #assert channels_create(token,name,is_public)
    p = requests.post(url + 'channels/create', json = param1)
    assert p.json()['code'] == 400

"""
    # test the owner is not in any channel
def test_channels_list_exc():
    #clear()
    requests.delete(url + 'clear')
    #token = "incorrect"
    param1 = {'token' : "incorrect"}
    with pytest.raises(AccessError):
        #assert channels_list(token)
        requests.get(url + 'channels/list', json = param1)

def test_channels_listall_exc(url):
    #clear()
    requests.delete(url + 'clear')
    #token = "incorrect"
    param1 = {'token' : "incorrect"}
    with pytest.raises(AccessError):
        #channels_listall(token)
        requests.get(url + 'channels/listall', json = param1)

def test_channels_createLongName(url):
    #clear()
    requests.delete(url + 'clear')
    #x = auth_register("test@gmail.com", "easypass", "Nick", "Sal")
    param1 = {'email' : "test@gmail.com", 'password' : "easypass", 'name_first' : "Nick", 'name_last' : "Sal"}
    x = requests.post(url + 'auth/register', json = param1)
    
    t1 = x.json()['token']
    param2 = {'token' : t1, 'name' : 'jadhbiushdbvweqrweqrqwghjaevwgfhehehjvrbwjuhy', 'is_public' : True}
    print(requests.post(url + 'channels/create', json = param2).json())
    with pytest.raises (InputError(400)) :
        #channels_create(t1,'jadhbiushdbvweqrweqrqwghjaevwgfhehehjvrbwjuhy',True)
        requests.post(url + 'channels/create', json = param2)

"""