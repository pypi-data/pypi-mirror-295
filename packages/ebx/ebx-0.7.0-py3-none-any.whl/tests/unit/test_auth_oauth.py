from ebx.auth import OAuthAuthentication
from ebx.config import ClientConfig
from ebx.persistence.in_memory import InMemoryPersistence
import os
import pytest
from ebx.constants.api import API_TOKEN_FILE
from .constants import AUTH_TOKEN_DATA
from pytest_httpx import HTTPXMock
from datetime import datetime, timezone

def test_cannot_create_oauth_no_details():
   
    persistence_driver = InMemoryPersistence()
    config = ClientConfig(persistence_driver=persistence_driver) 

    with pytest.raises(ValueError):
        auth = OAuthAuthentication(config)


def test_can_create_oauth_from_env():
    os.environ['EBX_CLIENT_ID'] = 'my_test_client_id'
    os.environ['EBX_CLIENT_SECRET'] = 'my_test'

    persistence_driver = InMemoryPersistence()
    config = ClientConfig(persistence_driver=persistence_driver) 

    auth = OAuthAuthentication(config)

    assert auth.client_id == 'my_test_client_id'
    assert auth.client_secret == 'my_test'

def test_can_create_oauth_from_values():
    client_id = 'my_test_client_id'
    client_secret = 'my_test'

    persistence_driver = InMemoryPersistence()
    config = ClientConfig(persistence_driver=persistence_driver) 

    auth = OAuthAuthentication(config, client_id=client_id, client_secret=client_secret)

    assert auth.client_id == client_id
    assert auth.client_secret == client_secret

def test_can_load_from_persistance():
    client_id = 'my_test_client_id'
    client_secret = 'my_test'

    saved_filename = f"{client_id}_{API_TOKEN_FILE}"
    persistence_driver = InMemoryPersistence()
    persistence_driver.save(saved_filename, AUTH_TOKEN_DATA.copy())

    config = ClientConfig(persistence_driver=persistence_driver) 

    auth = OAuthAuthentication(config, client_id=client_id, client_secret=client_secret)
    headers = auth.get_headers()

    assert auth.get_token_filename() == saved_filename
    assert headers['Authorization'] == f"Bearer {AUTH_TOKEN_DATA['token']}"


def test_can_refresh_oauth(httpx_mock: HTTPXMock):
    client_id = 'my_test_client_id'
    client_secret = 'my_test'
    new_access_token = AUTH_TOKEN_DATA['token']+ "_new"

    httpx_mock.add_response(json={
        "access_token": AUTH_TOKEN_DATA['token']+ "_new",
        "expires_in": '2021-01-01T00:00:00'
    })

    persistence_driver = InMemoryPersistence()

    config = ClientConfig(persistence_driver=persistence_driver) 
    auth = OAuthAuthentication(config, client_id=client_id, client_secret=client_secret)

    auth.refresh()

    headers = auth.get_headers()

    assert headers['Authorization'] == f"Bearer {new_access_token}"
    assert auth.auth_token.expires == datetime.fromisoformat('2021-01-01T00:00:00').replace(tzinfo=timezone.utc)
    assert persistence_driver.load(auth.get_token_filename())['token'] == new_access_token


    