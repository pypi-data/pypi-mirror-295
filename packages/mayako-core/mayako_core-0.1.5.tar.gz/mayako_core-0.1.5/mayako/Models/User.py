from dataclasses import dataclass, asdict
from typing import Dict, Self, Optional
from ..Config import CCLIENT

@dataclass
class User:
    """
    a model class which represents the inidividual machine

    as this project can be used by multiple users, we use this class to distinguish between users as the mac address is unique. this lets users have different arduino folders. uses mayako/Service/MacAddress.py to retrieve it.

    Attributes:
        user_mac_address (str): mac address with following schema: XX:XX:XX:XX:XX:XX
        arduino_folder (str): the path where the arduino project is located; improtant for mayako/Service/ArduinoUploader.py
    """
    user_mac_address: str
    arduino_folder: Optional[str] = CCLIENT.DEFAULT_ARDUINO_FOLDER

    def to_dict(self) -> Dict:
        """makes a dictionary from the class"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> Self:
        """returns an instance of the according class by passing a dictionary"""
        default_data = {
            "arduino_folder": CCLIENT.DEFAULT_ARDUINO_FOLDER
        }
        
        merged_data = {**default_data, **data}
        return cls(**merged_data)