from ..Config import CERROR_MESSAGES

class IdentitiyKeyUsedError(Exception):
    '''
    Expcetion raised when an identity key is used more than once.
    '''
    def __init__(self, identity_key: str) -> None:
        super().__init__(f'The identity key {identity_key} has already been used in another instance.')

class IdentitiyPatternError(Exception):
    '''
    Expcetion raised when an identity key is used more than once.
    '''
    def __init__(self, identity_key: str) -> None:
        super().__init__(f'The identity key {identity_key} must be between 2 and 8 characters long and may only contain underscores (_) as special characters.')