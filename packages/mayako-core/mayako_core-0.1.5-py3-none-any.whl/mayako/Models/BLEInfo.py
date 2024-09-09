from dataclasses import dataclass, asdict
from typing import List, Dict, Self

@dataclass
class BLEInfo:
    address: str
    name: str
    service_uuid: str
    characteristic_uuid: str

    def to_dict(self) -> Dict:
        """makes a dictionary from the instance"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> Self:
        """creates an instance of this class with information from a dictionary"""
        return cls(**data)