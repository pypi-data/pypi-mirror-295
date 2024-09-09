import json, struct

from .NetworkInterface import NetworkInterface
from crcmod import crcmod

class IntegrityMiddleware:

    counter: list[any]
    protocol: NetworkInterface

    def __init__(self, protocol: NetworkInterface) -> None:
        self.protocol = protocol
        

    def write(self) -> None:
        self.protocol.write()

    def read(self) -> None:
        self.protocol.read()

    def _calc_checksum(data: bytes) -> int:
        #https://crcmod.sourceforge.net/crcmod.html
        #crc16
        #TODO: check credentials
        return crcmod.mkCrcFun(0x11021, rev=False, initCrc=0x0000, xorOut=0x0000)