import re
from .Exceptions import *
from ..Config import CERROR_MESSAGES

class Identity:

    '''Identity manages identity keys to uniquely distinguish devices and other things.
    
    End Users do not explicitly use the Identity class, it is part of the devices

    Attributes:
        ACC_01 (str): An example for a class attribute which can be used as a identity key to name Sensors, Actuators, Microcontrollers or WiFiProfiles
        TEMP_01 (str): A second example
        WP_01 (str): Another example
    '''

    def __init__(self) -> None:
        '''Identity should not be instantiated to avoid double keys.'''
        raise NotImplementedError(CERROR_MESSAGES.CLASS_NO_INIT)

    #https://stackoverflow.com/a/71546645
    @classmethod
    def __str__(cls) -> None:
        '''Makes a report on the attributes used in the class.'''
        xs = []
        for name, value in vars(cls).items():
            if not (name.startswith('__') or isinstance(value, classmethod)):
                xs.append(value)
        return xs

    @classmethod
    def register(cls, identity: str) -> None:
        '''
        This function registers identity keys and throws if they are not unique.
        
        Identity keys are meant to be short to keep the syntax short.
        Identity keys are not meant for long description, in this case use the description attribute on the according classes.

        Identitiy may have 2 to 20 charactes that are a to z or numbers.

        Raises a custom exception if the attribute is already used.
        Raises a custom exception if the provided identity is empty or does not match the pattern.

        Args:
            identity (str): An identity key chosen by the end user to uniquely identify devices in the framework.
        '''
        if type(identity) is not str or identity == "":
            raise IdentitiyPatternError(identity)
        
        pattern = r'^[A-Za-z0-9_]{2,20}$'

        if not re.search(pattern, identity):
            raise IdentitiyPatternError(identity)

        if hasattr(cls, identity):
            raise IdentitiyKeyUsedError(identity)
        
        setattr(cls, identity, identity)