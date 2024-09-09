import time
import serial
from queue import Queue
import threading
from typing import Optional

from .NetworkInterface import NetworkInterface
from ..Config import CNETWORK, CPACKET
from .Packet import Packet

class Serial(NetworkInterface):
    """
    Source
        https://www.instructables.com/Starting-and-Stopping-Python-Threads-With-Events-i/
    """
    _serial_port: str
    _baud_rate: int
    _timeout: int
    _serial: serial.Serial
    _read_queue: Queue[Packet]
    _write_queue: Queue[Packet]
    _stop_event: threading.Event
    _thread: threading.Thread

    def __init__(self, serial_port: str, baud_rate: int = CNETWORK.BAUDRATE, timeout: int = CNETWORK.TIMEOUT) -> None:
        self._serial_port = serial_port
        self._baud_rate = baud_rate
        self._timeout = timeout
        self._serial = None
        self._read_queue = Queue()
        self._write_queue = Queue()
        self._stop_event = threading.Event()

    def connect(self) -> None:
        self._serial = serial.Serial(self._serial_port, self._baud_rate, timeout=self._timeout)

        self._stop_event.clear()#unset the flag

        self._read_thread = threading.Thread(target=self._read_data)
        self._write_thread = threading.Thread(target=self._write_data)

        self._read_thread.start()
        self._write_thread.start()

    def _read_data(self) -> None:
        while not self._stop_event.is_set():
            
            if self._serial.in_waiting > CPACKET.HEADER_SIZE:
                b = self._serial.read(size=1)
                validByte: bool = Packet.verify_flag(b)
                if not validByte:
                    continue

                headerData = self._serial.read(size=CPACKET.HEADER_SIZE)
                packet = Packet()
                packet.deserialize_header(headerData)

                payload_size: int = packet.get_payload_size()
                if self._serial.in_waiting < payload_size:
                    continue
                    
                payloadData = self._serial.read(payload_size)

                packet.deserialize_payload(payloadData)

                self._read_queue.put(packet)

            time.sleep(CNETWORK.BUSY_WAITING_TIMEOUT)
                

    def _write_data(self) -> None:
        while not self._stop_event.is_set():
            if not self._write_queue.empty():
                packet = self._write_queue.get()
                serialisedData = packet.serialize()

                self._serial.write(serialisedData)
            
            time.sleep(CNETWORK.BUSY_WAITING_TIMEOUT)

    def disconnect(self) -> None:
        self._stop_event.set()

        if self._read_thread.is_alive():
            self._read_thread.join()
        
        if self._write_thread.is_alive():
            self._write_thread.join()
        
        if self._serial:
            self._serial.close()

    def check_connection(self) -> bool:
        return True
    
    def get_protocol_name(self) -> str:
        return "Serial"

    def write(self, data: Packet) -> None:
        self._write_queue.put(data)

    def read(self) -> Optional[Packet]:
        if self._read_queue.qsize() > 0:
            return self._read_queue.get()

        return None