from ebx.models.oauth_client import OAuthClient
from ebx.config import ClientConfig
from ebx.persistence.in_memory import InMemoryPersistence
from .constants import OAUTH_CLIENT_DATA

def test_auth_client():
    client = OAuthClient(**OAUTH_CLIENT_DATA)
    assert client.name == OAUTH_CLIENT_DATA['name']
    assert client.description == OAUTH_CLIENT_DATA['description']
    assert client.client_id == OAUTH_CLIENT_DATA['client_id']
    assert client.client_secret == OAUTH_CLIENT_DATA['client_secret']
    assert client.enabled == OAUTH_CLIENT_DATA['enabled']

def test_can_save_auth_client():
    memory_persistence = InMemoryPersistence()
    config = ClientConfig(persistence_driver=memory_persistence)
    client = OAuthClient(**OAUTH_CLIENT_DATA)
    client.save(config,'test_save')
    assert memory_persistence.exists('test_save')

def test_can_load_auth_client():
    memory_persistence = InMemoryPersistence()
    memory_persistence.save('test_save', OAUTH_CLIENT_DATA.copy())

    config = ClientConfig(persistence_driver=memory_persistence)
    client = OAuthClient.load(config,'test_save')
    assert client.name == OAUTH_CLIENT_DATA['name']
    assert client.description == OAUTH_CLIENT_DATA['description']
    assert client.client_id == OAUTH_CLIENT_DATA['client_id']
    assert client.client_secret == OAUTH_CLIENT_DATA['client_secret']
    assert client.enabled == OAUTH_CLIENT_DATA['enabled']

def test_can_check_client_exists():
    memory_persistence = InMemoryPersistence()
    memory_persistence.save('test_save', OAUTH_CLIENT_DATA.copy())

    config = ClientConfig(persistence_driver=memory_persistence)
    assert OAuthClient.saved_credentials_exists(config,'test_save')