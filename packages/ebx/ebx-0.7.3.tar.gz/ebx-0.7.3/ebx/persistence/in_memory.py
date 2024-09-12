"""
----------------------------------------------------------------------------
COMMERCIAL IN CONFIDENCE

(c) Copyright Quosient Ltd. All Rights Reserved.

See LICENSE.txt in the repository root.
----------------------------------------------------------------------------
"""
from ebx.persistence.abstact_persistence import AbstractPersistence


class InMemoryPersistence(AbstractPersistence):
    """In Memory system persistence."""

    def __init__(self) -> None:
        super().__init__()
        self.MEMORY_PERISTENCE = {}

    def save(self,key:str, data):
        self.MEMORY_PERISTENCE[key] = data
        return self

    def exists(self, key: str) -> bool:
        return key in self.MEMORY_PERISTENCE
    
    def load(self, key: str):
        return self.MEMORY_PERISTENCE[key]
    
    def set_path(self, path: str):
        # noop
        return self