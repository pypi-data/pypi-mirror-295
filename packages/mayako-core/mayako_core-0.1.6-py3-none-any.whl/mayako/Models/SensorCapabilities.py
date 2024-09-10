from dataclasses import dataclass, asdict
from typing import Dict, Self

@dataclass
class SensorCapabilities:
    """
    a model class which contains capabilities of sensors.

    the capabilities do not include sensor data, only parameters which influence the record behaviour plus identity to indentify the sensor instance.

    Attributes:
        enable (bool): if a sensor is enabled for the record; default is True because when the sensor is created by the user, it is obvious that he wants to enable it. the sensors on the device are set to disabled per default only being enabled when an according capability is passed.
        sample_rate (int): data pointer recored per second
        data_on_state_change (bool): determines of data should be sent from the device if there is no change from the previous state; False => send all data; True => only when change
        identity (str): the identity of the sensor

    """
    identity: str
    sample_rate: int
    data_on_state_change: bool
    enable: bool = True
    include_timestamp: bool = False
    include_sequence: bool = False
    model_data: str = ""

    def to_dict(self) -> Dict:
        """makes a dictionary from the instance"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> Self:
        """
        makes an instance of the according class using a dictionary.

        not existing values are set to default values. identity must exist as it is an integral part.

        Args:
            data (Dict): dictionary with instance properties

        Returns:
            Self: an instance of the class with the assigned values
        """
        default_data = {
            'enable': True,
            'sample_rate': 10,
            'data_on_state_change': False,
            #identity must be provided
        }
        
        merged_data = {**default_data, **data}
        return cls(**merged_data)