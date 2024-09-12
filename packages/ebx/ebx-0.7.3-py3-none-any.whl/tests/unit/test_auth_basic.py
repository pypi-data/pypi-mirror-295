from ebx.auth import BasicAuth
from ebx.config import ClientConfig
import base64
import pytest

def test_can_create_basic_auth():
    username = 'test_user'
    password = 'test_password'

    # base64 encode the username and password
    base64string = base64.b64encode(f"{username}:{password}".encode('utf-8')).decode('utf-8')


    config = ClientConfig()

    auth = BasicAuth(config, email=username, password=password)
    headers = auth.get_headers()

    assert auth.has_expired() == False
    assert headers['Authorization'] == 'Basic ' + base64string


def test_cannot_refresh_basic_auth():
    username = 'test_user'
    password = 'test_password'

    config = ClientConfig()

    auth = BasicAuth(config, email=username, password=password)

    with pytest.raises(NotImplementedError):
        auth.refresh()

    