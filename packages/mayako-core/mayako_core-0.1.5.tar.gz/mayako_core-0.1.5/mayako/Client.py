import os
from typing import Callable, List, Dict
from queue import Queue
from enum import Enum
from pathlib import Path
from pynput.keyboard import Listener
import time
import threading
import json
import asyncio

from .Network import NetworkManager
from .Network.NetworkInterface import NetworkProtocols
from .Utils.Logger import LoggerInstance, LoggerType, LoggingLevel
from .Config import CCLIENT, CGENERAL, CNETWORK
from .MayakoData import MayakoData
from .Devices.MicroController import MicroController
from .Devices.Sensor import Sensor
from .Devices.Actuator import Actuator
from .Command.CustomCommands import CustomCommands
from .Command.StandardCommands import StandardCommands
from .Network.Packet import Packet
from .Models.Button import Button
from .Service.BLEScanner import scan_ble_addresses
from .Service.SerialScanner import scan_serial_ports
from .Network.BLE import BLE
from .Config import CPACKET
from .Network.NetworkManager import RecordStatus

class FileType(Enum):
    JSON="JSON"
    CSV="CSV"

class Client:

    _logger: LoggerType
    _port: int
    _debug: bool
    _path: str
    _config: dict
    _model: MayakoData
    _microcontrollers: Dict[str, NetworkManager]
    _sensors: List[Sensor]
    _actuators: List[Actuator]
    _commands: StandardCommands
    _custom_commands: CustomCommands
    _outgoing_network_queue: Queue[Packet]

    def __init__(self, port: int = CCLIENT.PORT, debug: bool = False, enable_ack: bool = False) -> None:
        self._port = port
        self._debug = debug
        self._enable_ack = enable_ack
        if CGENERAL.DEBUG or self._debug:
            LoggerInstance.init_logger(logging_level=LoggingLevel.DEBUG)
        else:
            LoggerInstance.init_logger()
        self._logger = LoggerInstance.get()
        self._model = MayakoData()
        self.record_status = RecordStatus.RECORD_INIT
        self.running = False
        self._run_interval = 0.01
        self._outgoing_network_queue = Queue()
        self._incoming_network_queue = Queue()
        self._microcontrollers = {}
        self._commands = StandardCommands(self._outgoing_network_queue)
        self._custom_commands = CustomCommands(self._outgoing_network_queue)
        self._start_callback = None
        self._stop_callback = None

    def register_key_for_exit(self, key: str = 'q') -> None:
        self._keyboard_listener = Listener(on_press=self._keyboard_callback)
        self._keyboard_listener.start()
        self._keyboard_key = key
    
    def _keyboard_callback(self, key) -> None:
        if hasattr(key, 'char') and key.char == self._keyboard_key:
            self._logger.debug("stopping record...")
            self._keyboard_listener.stop()
            self.stop_record()

    def use_microcontroller(self, mc_identity: str) -> MicroController:
        mc_capa = self._model.get_microcontroller_capa_by_identity(identity=mc_identity)
        if not mc_capa:
            raise Exception(f"the microcontroller with the provided identity {mc_identity} does not exist in {CCLIENT.CONFIG_FILE_NAME}. add a new device with the according identity in mayako-gui before proceeding.")
       
        mc = MicroController(mc_identity=mc_identity, model=self._model, custom_commands=self._custom_commands)
        
        mc_capa = mc.get_capabilities()
        ble_address = asyncio.run(scan_ble_addresses(mc_identity, timeout=2))
        if not ble_address:
            raise Exception(f"no BLE device with identity {mc_identity} found")
        
        nm = NetworkManager(mc_identity=mc_identity)
        nm.use_ble(ble_address=ble_address)
        nm.connect()
        
        self._microcontrollers[mc_identity] = nm

        return mc

    def start_gui(self) -> None:
        from .GUI.Views.MainView import MainView
        from .GUI.Controllers.MainController import MainController

        main_view = MainView()
        main_controller = MainController(main_view, self._model, self)
        
        main_controller.start()

    def save_data(self, file_path: str, file_type: FileType=FileType.JSON) -> None:
        self._logger.debug("saving file")
        """
        writes all sensor data to a file

        Todo:
            implement data dump to csv

        Sources:
            https://stackoverflow.com/a/62662388
        
        Args:
            file_path (str): the location where the file should be written; if the location is invalid, the Downloads folder will be chosen as a fallback solution
            file_type (FileType): choose the file format of the data file; supports csv and json
        """
        if file_type == FileType.JSON:
            all_data = self._model.dump_all_sensor_data_to_json()
            file_name = "data.json"
        elif file_type == FileType.CSV:
            all_data = self._model.dump_all_sensor_data_to_json()
            file_name = "data.json"
            self._logger.error("NYI")
            self._logger.error(f"filetype {file_type.name} not yet supported. falling back to json.")

        if not os.path.exists(file_path):
            fallback_path = str(Path.home() / "Downloads")

            if not os.path.exists(fallback_path):
                raise Exception(f"{file_path} does not exist. fallback soluation {fallback_path} did also not work")

            else:
                file_path = os.path.join(fallback_path, file_name)
        else:
            file_path = os.path.join(file_path, file_name)
            
        with open(file_path, "w") as file:
            file.write(all_data)
            file.close()
            self._logger.info(f"data written to {file_path}")

    def _run(self) -> None:
        while self.running:
            
            #was recevied from self.inc_queue
            """ b = Button(identity="BTN_01", is_pressed=True, timestamp=0, sequence=0)
            d = b.to_dict()
            j = json.dumps(d)

            packet = Packet()
            packet.set_method(0x21)
            packet.set_node_identity("NAKO")
            packet.set_payload(j)
            
            self._model.add_sensor_to_data_list("NAKO", "BTN_01")
            
            self._model.add_new_sensor_data(packet) """
            """
            stage 1: starts with start record
            scan BLE addresses
            scan serial addresses
            => determine the protocol used

            stage 2: update the capabilities found in mayakoData
            => wait for confirmation

            stage 3: start record
            => call _start_callback

            stage 4: record running
            => read sensor / write commands

            stage 5: sensors signal stop from their side/stop from users side
            => stop all records
            => call _stop_callback
            ===>>> or call stop record
            
            #always check capabilities before starting; always overwrite them from the mayako.json because we can not know if they have changed by someone or the user has changed... although we are aware that the user has changed?!...

            #for mc in self._microcontrollers:
            #    self._commands.record_start(mc._identity)
            """

            for _, mc in self._microcontrollers.items():
                packet = mc.read_data()
                if packet and packet.get_method() == CPACKET.METHOD_DATA:
                    self._model.add_new_sensor_data(packet)

            
            while not self._outgoing_network_queue.empty():
                output = self._outgoing_network_queue.get()

                self._microcontrollers[output.get_node_identity()].send_data(output)

            time.sleep(self._run_interval)

    def start_record(self) -> None:
        self.running = True
        for identity, _ in self._microcontrollers.items():
            self._commands.record_start(mc_identity=identity)
        
        self._thread = threading.Thread(target=self._run)
        self._thread.start()      

        if self._start_callback:
            self._start_callback()

    def stop_record(self) -> None:
        self._logger.debug("calling stop record")
        """this method stop the microcontrollers and calls the callback function register in on_stop"""
        
        for identity, mc in self._microcontrollers.items():
            self._commands.record_stop(mc_identity=identity)
            mc.disconnect()

        self.running = False
        
        if self.running:
            self.running = False
            self._thread.join()

        if self._stop_callback:
            self._stop_callback()

    def on_start(self, callback: Callable[[], None]) -> None:
        """registers a callback function that is called when the record has started"""
        self._start_callback = callback

    def on_stop(self, callback: Callable[[], None]) -> None:
        """registers a callback function that is called when all microcontrollers have stopped sending data"""
        self._stop_callback = callback
