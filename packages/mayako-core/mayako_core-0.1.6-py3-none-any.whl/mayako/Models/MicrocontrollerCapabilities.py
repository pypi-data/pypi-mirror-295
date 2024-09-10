from dataclasses import dataclass, asdict, field
from typing import Self, Dict, List, Optional
from ..Network.NetworkInterface import NetworkProtocols
from ..Models.SensorCapabilities import SensorCapabilities
from ..Models.ActuatorCapabilities import ActuatorCapabilities

@dataclass
class MicroControllerCapabilities:
    """
    Sources:
        https://stackoverflow.com/a/51976841
    """
    identity: str

    #these values influence the record
    include_timestamp: bool = False
    include_sequence: bool = False
    delay: int = 0
    duration: int = 0
    max_samples: int = 0

    #status
    online: bool = False
    wifi_key: Optional[str] = None  #this is only the wifi_key to the associated wifi_key
    serial_port: Optional[str] = None
    ble_address: Optional[str] = None
    battery_percentage: int = 0
    battery_charging: bool = False
    sensors: List[SensorCapabilities] = field(default_factory=list)
    actuators: List[ActuatorCapabilities] = field(default_factory=list)
    protocol: NetworkProtocols = field(default=NetworkProtocols.BLE)
    name: str = ""

    def format_string(self) -> str:
        """returns a string with a representation of the instance for Views"""
        return f"identity: {self.identity} -- protocol: {self.protocol.name} -- online: {self.online} -- serial port: {self.serial_port}"

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
            'include_timestamp': False,
            'include_sequence': False,
            'delay': 0,
            'duration': 0,
            'max_samples': 0,
            'online': False,
            'protocol': NetworkProtocols.BLE,
            'wifi_key': None,
            'serial_port': None,
            'ble_address': None,
            'battery_percentage': 0,
            'battery_charging': False,
            'name': "",
            'sensors': [],
            'actuators': []
            #identity must be provided
        }
        
        merged_data = {**default_data, **data}

        #ensure that proptocol is converted from string to enum
        if isinstance(merged_data['protocol'], str):
            merged_data['protocol'] = NetworkProtocols[merged_data['protocol']]

        merged_data['sensors'] = [
            SensorCapabilities(**sensor) if isinstance(sensor, dict) else sensor
            for sensor in merged_data['sensors']
        ]

        # Convert actuators from list of dicts to list of ActuatorCapabilities
        merged_data['actuators'] = [
            ActuatorCapabilities(**actuator) if isinstance(actuator, dict) else actuator
            for actuator in merged_data['actuators']
        ]
            
        return cls(**merged_data)