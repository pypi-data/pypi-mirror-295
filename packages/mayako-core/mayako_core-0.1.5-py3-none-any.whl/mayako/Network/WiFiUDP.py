import time
import socket
import threading
from queue import Queue
from typing import Optional

from .NetworkInterface import NetworkInterface
from ..Config import CNETWORK, CPACKET
from .Packet import Packet
from ..Utils.Logger import LoggerInstance, LoggerType

class WiFiUDP(NetworkInterface):

    _logger: LoggerType
    _server_ip: str
    _server_port: int
    _buffer_size: int
    _socket: socket.socket
    _read_queue: Queue[Packet]
    _write_queue: Queue[Packet]
    _stop_event: threading.Event
    _read_thread: threading.Thread
    _write_thread: threading.Thread

    def __init__(self, server_ip: str, server_port: int, buffer_size: int = CNETWORK.BUFFER_SIZE) -> None:
        self._logger = LoggerInstance.get()
        self._server_ip = server_ip
        self._server_port = server_port
        self._buffer_size = buffer_size
        self._socket = None
        self._read_queue = Queue()
        self._write_queue = Queue()
        self._stop_event = threading.Event()

    def connect(self) -> None:
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self._socket.bind((self._server_ip, self._server_port))
        except socket.error as e:
            if e.errno == CNETWORK.PORT_ALREADY_USED_CODE:
                self._logger.error("port already in use")
            else:
                self._logger.error(f"error connecting to socket: {e}")
            
            return

        self._stop_event.clear()

        self._read_thread = threading.Thread(target=self._read_data)
        self._write_thread = threading.Thread(target=self._write_data)

        self._read_thread.start()
        self._write_thread.start()

    def _read_data(self):
        while not self._stop_event.is_set():
            try:
                if self._sock:
                    data, _ = self._sock.recvfrom(self._buffer_size)
                    if len(data) > CPACKET.HEADER_SIZE:
                        packet = Packet()
                        packet.deserialize_header(data[:CPACKET.HEADER_SIZE])
                        packet.deserialize_payload(data[CPACKET.HEADER_SIZE:])
                        self._read_queue.put(packet)
            except socket.error as e:
                self._logger.error(f"UDP error during read: {e}")
                break

            time.sleep(CNETWORK.BUSY_WAITING_TIMEOUT)

    def _write_data(self):
        while not self._stop_event.is_set():
            try:
                if not self._write_queue.empty():
                    packet = self._write_queue.get()
                    serialized_data = packet.serialize()

                    if self._sock:
                        self._sock.sendto(serialized_data, (self._udp_ip, self._udp_port))
            except socket.error as e:
                self._logger.error(f"UDP error during write: {e}")
                break

            time.sleep(CNETWORK.BUSY_WAITING_TIMEOUT)

    def disconnect(self) -> None:
        self._stop_event.set()

        if self._read_thread and self._read_thread.is_alive():
            self._read_thread.join()

        if self._write_thread and self._write_thread.is_alive():
            self._write_thread.join()

        if self._socket:
            self._socket.close()
            self._socket = None

    def write(self, data: bytes) -> None:
        self._write_queue.put(data)

    def read(self) -> bytes:
        if self._read_queue.qsize() > 0:
            return self._read_queue.get()

        return None