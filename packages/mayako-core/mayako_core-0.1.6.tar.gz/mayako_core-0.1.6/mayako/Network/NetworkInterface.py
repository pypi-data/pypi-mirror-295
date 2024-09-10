from abc import ABC, abstractmethod
from enum import Enum
from ..Network.Packet import Packet
from typing import Optional

class NetworkProtocols(str, Enum):
    """
    Indicates the Network Protocol in MicrocontrollerCapabilities
    
    Sources:
        https://stackoverflow.com/a/51976841
    """
    WIFI="WIFI"
    BLE="BLE"
    SERIAL="SERIAL"

class NetworkInterface(ABC):

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass

    @abstractmethod
    def write(self, data: Packet) -> None:
        pass

    @abstractmethod
    def read(self) -> Optional[Packet]:
        pass

    @abstractmethod
    def check_connection(self) -> bool:
        pass
    
    @abstractmethod
    def get_protocol_name(self) -> str:
        pass