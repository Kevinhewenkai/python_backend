import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests
import json
from help_functions import generate_token

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

def test_register_users(url):
    requests.post(url + 'auth/register', json = default_user)
    requests.post(url + 'auth/register', json = default_user2)
    requests.post(url + 'auth/register', json = default_user3)

def test_http_invalid_email(url):
    
    resp = requests.post(url + 'auth/register', json = {'email': 'notvalidemail.com', 'password': 'password123', 'name_first': 'Vince', 'name_last': 'Lam'})
    assert resp.json()['code'] == 400

    resp = requests.post(url + 'auth/login', json = {'email': 'notvalidemail.com', 'password': 'password123'})
    assert resp.json()['code'] == 400
    
    resp = requests.post(url + 'auth/passwordreset/request', json = {'email': 'notvalidemail.com'})
    assert resp.json()['code'] == 400


def test_http_used_email(url):

    resp = requests.post(url + 'auth/register', json = {'email': "testgmail.com", 'password': "password123!", 'name_first': "kanye", 'name_last': "west"})
    assert resp.json()['code'] == 400

def test_http_wrong_password(url):

    resp = requests.post(url + 'auth/login', json = {'email': 'test@gmail.com', 'password': 'wrongpass123'})
    assert resp.json()['code'] == 400

def test_http_unused_email_login(url):

    resp = requests.post(url + 'auth/login', json = {'email': 'unused@gmail.com', 'password': 'password123!'})
    assert resp.json()['code'] == 400

def test_http_failed_logout(url):
    resp = requests.post(url + 'auth/logout', json = {'token': 'badtoken'})
    assert resp.json()['code'] == 400

def test_http_password_length(url):
    resp = requests.post(url + 'auth/register', json = {'email': "kanye@gmail.com", 'password': "short", 'name_first': "kanye", 'name_last': "west"})
    assert resp.json()['code'] == 400

    resp = requests.post(url + 'auth/passwordreset/request', json = {'email': "kanye@gmail.com", 'password': "short", 'name_first': "kanye", 'name_last': "west"})
    assert resp.json()['code'] == 400

def test_http_length_of_names(url):
    resp = requests.post(url + 'auth/register', json = {'email': "kanye@gmail.com", 'password': "password123!", 'name_first': "", 'name_last': "west"})
    assert resp.json()['code'] == 400

    resp = requests.post(url + 'auth/register', json = {'email': "kanye@gmail.com", 'password': "password123!", 'name_first': "kanye", 'name_last': ""})
    assert resp.json()['code'] == 400

def test_htttp_wrong_username(url):
    resp = requests.post(url + 'auth/login', json = {'email': "test@gmail.com", 'password': "wrongpass"})
    assert resp.json()['code'] == 400

def test_http_auth_register(url):
    requests.delete(url + 'clear')
    resp = requests.post(url + 'auth/register', json = {'email': 'test@gmail.com', 'password': 'password123', 'name_first': 'Vince', 'name_last': 'Lam'})
    assert resp.json() == {'u_id': 0, 'token': generate_token(0)}
