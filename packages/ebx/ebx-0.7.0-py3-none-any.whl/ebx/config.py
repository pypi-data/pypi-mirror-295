"""
----------------------------------------------------------------------------
COMMERCIAL IN CONFIDENCE

(c) Copyright Quosient Ltd. All Rights Reserved.

See LICENSE.txt in the repository root.
----------------------------------------------------------------------------
"""
from ebx.constants.api import API_PREFIX, OAUTH_PATH, BASE_URL, API_SECRETS_PATH
import urllib.parse
from os import getenv
from ebx.persistence.local_filesystem import LocalFilePersistence
from ebx.persistence.abstact_persistence import AbstractPersistence

class ClientConfig():
    """Configuration for the Earth Blox API client, connecting to the versioned API for non-auth endpoints."""

    base_url: str
    """The base url for the API"""

    api_prefix: str
    """The version prefix for the API"""

    oauth_path: str
    """The path for the oauth flow"""

    persistence_driver: AbstractPersistence
    """The persistence driver for storing credentials"""

    request_timeout: int = 10
    """The request timeout for the client"""

    def __init__(self, 
                 base_url: str = BASE_URL, 
                 api_prefix: str = API_PREFIX, 
                 oauth_path: str = OAUTH_PATH, 
                 persistence_driver: AbstractPersistence = LocalFilePersistence(path=API_SECRETS_PATH),
                 request_timeout: int = 10
    ) -> None:
        """Initialise the base configuration for a client."""
        self.base_url = base_url
        self.api_prefix = api_prefix
        self.oauth_path = oauth_path 
        self.persistence_driver = persistence_driver
        self.request_timeout = request_timeout

        if getenv("EBX_API_EMULATOR_HOST") is not None:
            emulator_host = getenv("EBX_API_EMULATOR_HOST")
            self.base_url = emulator_host
        elif getenv("EBX_API_BASE_URL") is not None:
            self.base_url = getenv("EBX_API_BASE_URL")
        
        if getenv("EBX_API_PREFIX_PATH") is not None:
            self.api_prefix = getenv("EBX_API_PREFIX_PATH")

    def get_api_base_url(self) -> str:
        """Returns the base url for the API, including the version prefix."""
        return urllib.parse.urljoin(self.base_url, self.api_prefix)
    
    def get_oauth_url(self) -> str:
        """Returns the url for the oauth flow, excludes the version prefix."""
        if getenv("EBX_API_AUTH_EMULATOR") is not None:
           return getenv("EBX_API_AUTH_EMULATOR")  
        return urllib.parse.urljoin(self.base_url, self.oauth_path)
    
    def get_persistence_driver(self) -> AbstractPersistence:
        """Returns the persistence driver for storing credentials."""
        return self.persistence_driver
    
    def get_request_timeout(self) -> int:
        """Returns the request timeout for the client."""
        return self.request_timeout
    
    def __str__(self) -> str:
        """Returns a string representation of the config, called if you print the object."""
        return f"ClientConfig(base_url={self.base_url}, api_prefix={self.api_prefix}, oauth_path={self.oauth_path}, persistence_driver={self.persistence_driver})"

class ServiceClientConfig(ClientConfig):
    """Configuration for the Earth Blox API client connecting to auth endpoints, without the versioned API prefix."""
    def __init__(self) -> None:
        super().__init__()
        self.api_prefix = ""
        self.base_url = BASE_URL
        
        if getenv("EBX_API_CLIENT_REGISTRATION") is not None:
            emulator_host = getenv("EBX_API_CLIENT_REGISTRATION")
            self.base_url = emulator_host 
        elif getenv("EBX_API_BASE_URL") is not None:
            self.base_url = getenv("EBX_API_BASE_URL")