from dataclasses import dataclass, asdict
from typing import Dict, Self
@dataclass
class ActuatorCapabilities:
    """
    a model class which contains capabilities of actuators.

    the capabilities only contain parameters which influence the record behaviour plus identity to indentify the actuator instance.

    Attributes:
        enable (bool): if a actuator is enabled for the record; default is True because when the actuator is created by the user, it is obvious that he wants to enable it. the actuators on the device are set to disabled per default only being enabled when an according capability is passed.
        identity (str): the identity of the actuator

    """
    identity: str
    enable: bool = True
    commands: str = ""

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
            #identity must be provided
        }
        
        merged_data = {**default_data, **data}
        return cls(**merged_data)