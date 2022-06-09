import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests
import json
from help_functions import generate_token
from requests.exceptions import HTTPError

default_user = {
    'email': "test@gmail.com",
    'password': "password123!",
    'name_first': "kanye",
    'name_last': "west"
}

default_user2 = {
    'email': "test2@gmail.com",
    'password': "password123!",
    'name_first': "kanyetwo",
    'name_last': "westtwo"
}

default_user3 = {
    'email': "test3@gmail.com",
    'password': "password123!",
    'name_first': "kanyethree",
    'name_last': "westthree"
}

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

def test_htttp_wrong_types(url):
    requests.delete(url + 'clear')
    x = requests.post(url + 'auth/register', json = default_user)
    token = x.json()['token']

    with pytest.raises(HTTPError):
        requests.get(url + 'user/profile', json = {'token': token, 'u_id': 1.2}).raise_for_status()
    
    with pytest.raises(HTTPError):
        requests.get(url + 'user/profile', json = {'token': 2, 'u_id': 2}).raise_for_status()
    
    with pytest.raises(HTTPError):
        requests.get(url + 'user/profile', json = {'token': token, 'u_id': -12}).raise_for_status()

def test_http_invalid_token_uid(url):
    requests.delete(url + 'clear')
    x = requests.post(url + 'auth/register', json = default_user2)
    token = x.json()['token']
    uid = x.json()['u_id']

    with pytest.raises(HTTPError):
        requests.get(url + 'user/profile', json = {'token': "thisiswrong", 'u_id': uid}).raise_for_status()
    
    with pytest.raises(HTTPError):
        requests.get(url + 'user/profile', json = {'token': token, 'u_id': 3}).raise_for_status()

def test_http_too_long(url):
    requests.delete(url + 'clear')
    x = requests.post(url + 'auth/register', json = default_user3)
    token = x.json()['token']

    with pytest.raises(HTTPError):
        requests.put(url + 'user/profile/setname', json = {'token': token, 'name_first': "kanyekanyekanyekanyekanyekanyekanyekanyekanyekanye12", 
                                                            'name_last': "west"}).raise_for_status()
    
    with pytest.raises(HTTPError):
        requests.put(url + 'user/profile/setname', json = {'token': token, 'name_first': "kanye", 
                                                            'name_last': "WestWestWestWestWestWestWestWestWestWestWestWestWest"}).raise_for_status()

def test_http_too_short(url):
    requests.delete(url + 'clear')
    x = requests.post(url + 'auth/register', json = default_user)
    token = x.json()['token']

    with pytest.raises(HTTPError):
        requests.put(url + 'user/profile/setname', json = {'token': token, 'name_first': "", 'name_last': "west"}).raise_for_status()

    with pytest.raises(HTTPError):
        requests.put(url + 'user/profile/setname', json = {'token': token, 'name_first': "kanye", 'name_last': ""}).raise_for_status()

def test_http_invalid_email(url):
    requests.delete(url + 'clear')
    x = requests.post(url + 'auth/register', json = default_user2)
    token = x.json()['token']

    with pytest.raises(HTTPError):
        requests.put(url + 'user/profile/setemail', json = {'token': token, 'email': "1234567.com"}).raise_for_status()

def test_http_wrong_token(url):
    requests.delete(url + 'clear')
    requests.post(url + 'auth/register', json = default_user)
    x = requests.post(url + 'auth/register', json = default_user2)
    token = x.json()['token']

    with pytest.raises(HTTPError):
        requests.put(url + 'user/profile/setemail', json = {'token': token, 'email': "test@gmail.com"}).raise_for_status()

def test_http_short_handle(url):
    requests.delete(url + 'clear')
    x = requests.post(url + 'auth/register', json = default_user)
    token = x.json()['token']

    with pytest.raises(HTTPError):
        requests.put(url + 'user/profile/sethandle', json = {'token': token, 'handle_str': "hw"}).raise_for_status()

def test_http_long_handle(url):
    requests.delete(url + 'clear')
    x = requests.post(url + 'auth/register', json = default_user)
    token = x.json()['token']

    with pytest.raises(HTTPError):
        requests.put(url + 'user/profile/sethandle', json = {'token': token, 'handle_str': "qwertyuiopasdfghjklzxcvbnm"}).raise_for_status()

def test_http_same_handle(url):
    requests.delete(url + 'clear')
    x = requests.post(url + 'auth/register', json = default_user)
    token = x.json()['token']

    with pytest.raises(HTTPError):
        requests.put(url + 'user/profile/sethandle', json = {'token': token, 'handle_str': "kanyewest"}).raise_for_status()

