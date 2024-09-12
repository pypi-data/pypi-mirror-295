from ebx.auth import EnvAuthentication
from ebx.config import ClientConfig
import os

def test_can_create_env_auth():
    os.environ['EBX_API_TOKEN'] = 'my_test_token'
    
    config = ClientConfig()

    auth = EnvAuthentication(config)
    auth.refresh()
    headers = auth.get_headers()

    assert auth.has_expired() == False
    assert auth.auth_token == 'my_test_token'
    assert headers['Authorization'] == 'Bearer my_test_token'
    