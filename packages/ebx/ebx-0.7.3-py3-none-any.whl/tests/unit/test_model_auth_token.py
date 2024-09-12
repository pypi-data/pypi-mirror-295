from ebx.models.auth_token import AuthToken
from ebx.config import ClientConfig
from ebx.persistence.in_memory import InMemoryPersistence
from .constants import AUTH_TOKEN_DATA

def test_auth_token():
    token = AuthToken(**AUTH_TOKEN_DATA.copy())
    assert token.token == AUTH_TOKEN_DATA['token']
    assert token.expires.isoformat() == AUTH_TOKEN_DATA['expires']

def test_can_save_auth_token():
    memory_persistence = InMemoryPersistence()
    config = ClientConfig(persistence_driver=memory_persistence)
    token = AuthToken(**AUTH_TOKEN_DATA.copy())
    token.save(config,'test_save')
    assert memory_persistence.exists('test_save')

def test_can_load_auth_token():
    memory_persistence = InMemoryPersistence()
    memory_persistence.save('test_save', AUTH_TOKEN_DATA.copy())

    config = ClientConfig(persistence_driver=memory_persistence)
    token = AuthToken.load(config,'test_save')
    assert token.token == AUTH_TOKEN_DATA['token']
    assert token.expires.isoformat() == AUTH_TOKEN_DATA['expires']

def test_can_check_token_exists():
    memory_persistence = InMemoryPersistence()
    memory_persistence.save('test_save', AUTH_TOKEN_DATA.copy())

    config = ClientConfig(persistence_driver=memory_persistence)
    assert AuthToken.saved_token_exists(config,'test_save')