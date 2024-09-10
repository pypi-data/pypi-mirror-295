from bleak import BleakClient
import asyncio
from queue import Queue
import threading
from typing import Optional

from .NetworkInterface import NetworkInterface
from ..Config import CNETWORK, CPACKET
from .Packet import Packet
from ..Utils.Logger import LoggerInstance, LoggerType

class BLE(NetworkInterface):
    """
    Source
        https://www.instructables.com/Starting-and-Stopping-Python-Threads-With-Events-i/
        https://stackoverflow.com/a/68121144
        https://docs.python.org/3/library/asyncio-eventloop.html
        https://stackoverflow.com/a/71489745
    """
    _logger: LoggerType
    _address: str
    _service_uuid : str
    _characteristic_uuid: str
    _timeout: int
    _client: BleakClient
    _read_queue: Queue[Packet]
    _write_queue: Queue[Packet]
    _loop: asyncio.AbstractEventLoop
    _thread: threading.Thread
    _connected: bool
    _received_data: bytearray
    _expected_payload_size = Optional[int]

    def __init__(self, address: str, service_uuid: str, characteristic_uuid: str, timeout: int = CNETWORK.TIMEOUT) -> None:
        self._address = address
        self._service_uuid = service_uuid
        self._characteristic_uuid = characteristic_uuid
        self._timeout = timeout
        self._logger = LoggerInstance.get()
        self._client = BleakClient(self._address, timeout=self._timeout)
        self._read_queue = Queue()
        self._write_queue = Queue()
        self._loop = asyncio.new_event_loop()
        self._thread = None
        self._connected = False
        self._received_data = bytearray()
        self._expected_payload_size = None

    def connect(self) -> None:
        if self._thread and self._thread.is_alive():
            self._logger.debug("BLE: thread was still alive")
            self._thread.join()

        self._thread = threading.Thread(target=self._start_event_loop)
        self._thread.start()
    
    def _start_event_loop(self):
        # Create a new event loop for this thread
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._loop.run_until_complete(self._handle_device())

    async def _handle_device(self) -> None:
        try:
            await self._connect_client()

            if self._connected:
                notify_task = self._loop.create_task(self._start_notify())
                write_task = self._loop.create_task(self._write_data())

                await asyncio.gather(notify_task, write_task)

        except asyncio.CancelledError:
            self._logger.error(f"BLE: stop notify failed: asyncio.CancelledError")
        finally:
            await self._stop_notify()
            await self._client.disconnect()

    async def _connect_client(self) -> None:
        try:
            await self._client.connect()
            await self._client.get_services()
            self._connected = self._client.is_connected
            self._logger.debug("BLE: connected")
        except Exception as e:
            self._logger.error(f"BLE: connecting client failed: {e}")
            self._connected = False
            
    async def _start_notify(self):
        try:
            await self._client.start_notify(self._characteristic_uuid, self._notification_handler)
        except Exception as e:
            self._logger.error(f"BLE: start notify failed: {e}")

    async def _stop_notify(self):
        try:
            await self._client.stop_notify(self._characteristic_uuid)
        except Exception as e:
            self._logger.error(f"BLE: stop notify failed: {e}")
    
    def _notification_handler(self, sender: str, data: bytes):
        """Handles incoming BLE data and defragments it if needed."""
        # Append current data to accumulated packet
        self._received_data.extend(data)

        # If we don't know the expected payload size yet, calculate it from the header
        if self._expected_payload_size is None and len(self._received_data) >= CPACKET.HEADER_SIZE:
            # Assuming the payload size is stored in the header at bytes 8-10
            self._expected_payload_size = int.from_bytes(self._received_data[8:10], byteorder='big')
            #self._logger.debug(f"Expected payload size: {self._expected_payload_size}")

        # Check if we've received the full packet
        if self._expected_payload_size and len(self._received_data) >= self._expected_payload_size:
            # Full packet has been received, process it
            self._process_complete_packet(self._received_data)
            self._received_data.clear()  # Clear buffer for next packet
            self._expected_payload_size = None  # Reset for the next packet

    def _process_complete_packet(self, packet: bytearray):
        """Processes the complete packet after defragmentation."""
        #self._logger.debug("Complete packet received:")
        if len(packet) < CPACKET.HEADER_SIZE:
            self._logger.debug("BLE: packet too small to be valid")
            return
        
        try:
            # Deserialize packet header and payload
            header_data = packet[:CPACKET.HEADER_SIZE]
            payload_data = packet[CPACKET.HEADER_SIZE:]

            pkt = Packet()
            pkt.deserialize_header(header_data)
            pkt.deserialize_payload(payload_data)

            # Push the fully received and processed packet into the read queue

            self._read_queue.put(pkt)
            
        except Exception as e:
            self._logger.error(f"BLE: Error processing packet: {e}")

    async def _write_data(self) -> None:
        while self._connected:
            if not self._write_queue.empty():
                packet = self._write_queue.get()
                serialised_data = packet.serialize()

                try:
                    await self._client.write_gatt_char(self._characteristic_uuid, serialised_data)
                except Exception as e:
                    self._logger.error(f"BLE: failed writing data: {e}")
                    pass

            await asyncio.sleep(CNETWORK.BUSY_WAITING_TIMEOUT)

    def disconnect(self) -> None:
        if self._connected:
            self._connected = False  # Set connected status to False
            # Gracefully stop the BLE connection in the asyncio loop
            asyncio.run_coroutine_threadsafe(self._disconnect_client(), self._loop)

        if self._thread and self._thread.is_alive():
            self._thread.join()

        if self._loop.is_running():
            self._loop.run_until_complete(self._loop.shutdown_asyncgens())
            self._loop.stop()

        self._loop.close()
        self._logger.debug("BLE: network connection was closed")

    async def _disconnect_client(self) -> None:
        try:
            await self._stop_notify()
            await self._client.disconnect()
        except Exception as e:
            self._logger.error(e)

    def write(self, data: Packet) -> None:
        self._write_queue.put(data)

    def read(self) -> Optional[Packet]:
        if self._read_queue.qsize() > 0:            
            return self._read_queue.get()

        return None

    def check_connection(self) -> bool:
        return self._connected
    
    def get_protocol_name(self) -> str:
        return CNETWORK.BLE_NAME