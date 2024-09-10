from dataclasses import dataclass, asdict
from typing import Dict, Self

@dataclass
class SerialInfo:
    """
    the is a model class representing serial information retrieved with mayako/Service/SerialScanner.py

    Attributes:
        port (str): the serial port on the target machine; Example: /dev/ttyUSB0
        serial_number (str): a 8 byte hex; may be empty
        description (str): describes the connected device e.g. information about the technology, the kind of device, etc.; may be empty
    """
    port: str
    serial_number: str
    description: str

    def format_string(self) -> str:
        """
        makes a string from the properties of the class.
        
        Returns:
            str: a visual representation of the class used in Views
        """
        return f"Port: {self.port} -- Serial Number: {self.serial_number}"
    
    def to_dict(self) -> Dict:
        """makes a dictionary from the class"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> Self:
        """creates an instance of this class with information from a dictionary"""
        return cls(**data)