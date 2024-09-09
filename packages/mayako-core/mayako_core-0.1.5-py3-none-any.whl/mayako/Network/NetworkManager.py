from enum import Enum
from typing import List, Dict, Union, Optional, TypeVar, Generic

from ..Network.IntegrityMiddleware import IntegrityMiddleware
from ..Network.NetworkInterface import NetworkInterface
from ..Network.BLE import BLE
from ..Network.WiFiUDP import WiFiUDP
from ..Network.Serial import Serial
from ..Utils.Logger import LoggerInstance, LoggerType
from ..Models.SerialInfo import SerialInfo
from ..Models.BLEInfo import BLEInfo
from ..Models.WiFiProfile import WiFiProfile
from ..Network.Packet import Packet
from ..Network.NetworkInterface import NetworkProtocols

#https://stackoverflow.com/a/51976841

class RecordStatus(Enum):
    RECORD_INIT=0
    PROTOCOL_DETERMINED=1
    CAPABILITY_UPDATED=2
    RECORD_STARTED=3
    STOP_SIGNALED=4
    RECORD_STOPPED=5

class NetworkManager:

    _logger: LoggerType
    _mc_identity: str
    _network_protocol: NetworkProtocols
    _record_status: RecordStatus
    _network_implementation: NetworkInterface
    #_integrity_middelware: IntegrityMiddleware

    def __init__(self, mc_identity: str) -> None:
        self._logger = LoggerInstance.get()
        self._mc_identity = mc_identity
        self._network_protocol = None
        self._record_status = RecordStatus.RECORD_INIT
        self._network_implementation = None
        #self._integrity_middelware = IntegrityMiddleware(self._protocol)

    def use_serial(self, serial_address: SerialInfo) -> None:
        self._network_protocol = NetworkProtocols.SERIAL
        self._serial_address = serial_address
        self._network_implementation = Serial(serial_port=self._serial_address.port)

    def use_ble(self, ble_address: BLEInfo) -> None:
        self._network_protocol = NetworkProtocols.BLE
        self._ble_address = ble_address
        self._network_implementation = BLE(address=self._ble_address.address, service_uuid=self._ble_address.service_uuid, characteristic_uuid=self._ble_address.characteristic_uuid)

    def get_mc_identity(self) -> str:
        return self._mc_identity

    def use_wifi(self, wifi_profile: WiFiProfile) -> None:
        raise NotImplementedError
    
    def connect(self) -> None:
        self._network_implementation.connect()
    
    def send_data(self, packet: Packet) -> None:
        self._network_implementation.write(packet)
    
    def read_data(self) -> Optional[Packet]:
        return self._network_implementation.read()
    
    def disconnect(self) -> None:
        self._network_implementation.disconnect()

    def check_connection(self) -> bool:
        return self._network_implementation.check_connection()
    
    def get_protocol_name(self) -> str:
        return self._network_implementation.get_protocol_name()