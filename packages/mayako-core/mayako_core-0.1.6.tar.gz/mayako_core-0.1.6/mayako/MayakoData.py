import json
from typing import List, Dict, Optional
import os

from .Observable import Observable
from .Models.WiFiProfile import WiFiProfile
from .Service.SerialScanner import SerialInfo
from .Service.BLEScanner import BLEInfo
from .Models.User import User
from .Models.MicrocontrollerCapabilities import MicroControllerCapabilities
from .Models.SensorCapabilities import SensorCapabilities
from .Models.ActuatorCapabilities import ActuatorCapabilities
from .Config import CCLIENT
from .Utils.Logger import LoggerType, LoggerInstance
from .Service.MacAdress import get_macaddress
from .Network.Packet import Packet
from .Models.BaseDataModel import BaseDataModel

class MayakoData(Observable):

    """
    this is the central model class in mayako-core observable to GUI and Client

    Attributes:
        logger (LoggerType): instance of logger class
        this_user (User): the current user identified by the machine MAC address
        all_users (List[User]): all users that have worked on different machines in this project
        wifi_profile (List[WiFiProfiles]): list of wifi profiles created in mayako GUI
        serial_ports (List[SerialInfo]): list of serial access info that is retrieved with SerialScanner.py
        ble_addresses (List[BLEInfo]): list of BLE addresses retrieved with BLEScanner.py
        mc_capabilities (List[MicroControllerCapabilities]): all microcontrollers capabilities
        data: Dict[str, Dict[str, Dict[str, List[Dict]]]]: sensor data that is sorted by mc_identity and sensor_identity
        selected_wifi_profile (WiFiProfie): the wifi_profile selected in GUI which is loaded into the EditWiFiProfileView
        selected_mc_capability (MicroControllerCapabilities): the MicroControllerCapabilities selected in GUI which is loaded into DeviceDetailsView

    Example:
        data: the data is cast to the associated model class when it is transfered to the sensors themselves
        
        .. code-block: python
            {
                "MC01": {
                    "TEMP01": {
                        "data": [{"identity": "TEMP_01","temperature": 24.22}],
                        "last_accessed_index": 0
                    }
                    "ACC01": []
                }
            }
    """

    logger: LoggerType
    this_user: User
    all_users: List[User]
    wifi_profiles: List[WiFiProfile]
    serial_ports: List[SerialInfo]
    ble_addresses: List[BLEInfo]
    mc_capabilities: List[MicroControllerCapabilities]#sensor and actuator capabilities are in mc_capabilities
    data: Dict[str, Dict[str, Dict[str, List[Dict]]]]
    selected_wifi_profile: WiFiProfile
    selected_mc_capability: MicroControllerCapabilities
    

    def __init__(self) -> None:
        super().__init__()
        self.logger = LoggerInstance.get()
        self.this_user = None
        self.all_users = []
        self.wifi_profiles = []
        self.serial_ports = []
        self.ble_addresses = []
        self.mc_capabilities = []
        self.data = {}
        self.selected_wifi_profile = None
        self.selected_mc_capability = None

        self._check_if_file_exists()
        self._load_from_file()
        self._check_if_user_exists()
        self._save_to_file()


        self._self_bind()

    def _check_if_file_exists(self) -> None:
        curr_workdir = os.getcwd()
        config_file_path = os.path.join(curr_workdir, CCLIENT.CONFIG_FILE_NAME)
        
        if not os.path.exists(config_file_path):
            with open(config_file_path, "w") as file:
                file.write("{}")
        else:
            self.logger.debug(f"{CCLIENT.CONFIG_FILE_NAME} already exists")

    def _check_if_user_exists(self) -> None:
        if not self.this_user:
            pass

    def _load_from_file(self) -> None:
        with open(CCLIENT.CONFIG_FILE_NAME, "r") as file:
            data = json.load(file)
            
            if "wifi_profiles" in data:
                # Load wifi profiles
                wifi_profiles = [WiFiProfile.from_dict(wifi_profile) for wifi_profile in data["wifi_profiles"]]
                self.add_wifi_profile(wifi_profiles)
            
            if "ble_addresses" in data:
                # Load BLE addresses
                ble_addresses = [BLEInfo.from_dict(item) for item in data["ble_addresses"]]
                self.add_ble_address(ble_addresses)
            
            if "microcontroller_capas" in data:
                # Load microcontrollers
                microcontroller_capas = [MicroControllerCapabilities.from_dict(item) for item in data["microcontroller_capas"]]
                self.add_microcontroller_capa(microcontroller_capas)
            
            if "users" in data:
                # Load users
                self.all_users = [User.from_dict(u) for u in data["users"]]
            
            self.this_user = self._check_user(self.all_users)

    def _save_to_file(self, *_) -> None:
        d = {
            "users": [],
            "wifi_profiles": [],
            "ble_addresses": [],
            "microcontroller_capas": []
        }

        for user in self.all_users:
            d["users"].append(user.to_dict())
        
        for wifi_profile in self.wifi_profiles:
            d["wifi_profiles"].append(wifi_profile.to_dict())

        for ble_address in self.ble_addresses:
            d["ble_addresses"].append(ble_address.to_dict())

        for microcontroller_capa in self.mc_capabilities:
            d["microcontroller_capas"].append(microcontroller_capa.to_dict())

        with open(CCLIENT.CONFIG_FILE_NAME, "w") as file:
            json.dump(d, file, indent=4)

    def _self_bind(self) -> None:
        self.subscribe("wifi_profiles_update", self._save_to_file)
        self.subscribe("microcontroller_capa_update", self._save_to_file)
        self.subscribe("serial_ports_update", self._save_to_file)
        self.subscribe("user_update", self._save_to_file)
        self.subscribe("ble_addresses_update", self._save_to_file)

    def _check_user(self, users: List[User]) -> User:
        user_address = get_macaddress()
        user = None
    
        for u in users:
            if u.user_mac_address == user_address:
                user = u
                return user
        
        new_user = User(user_mac_address=user_address, arduino_folder=CCLIENT.DEFAULT_ARDUINO_FOLDER)

        if new_user not in self.all_users:
            self.all_users.append(new_user)
            
        return new_user

    def add_wifi_profile(self, wifi_profiles: List[WiFiProfile]) -> None:
        for wifi_profile in wifi_profiles:
            if wifi_profile in self.wifi_profiles:
                continue
            
            self.wifi_profiles.append(wifi_profile)

        self._notify_observers("wifi_profiles_update")

    def remove_wifi_profile(self, wifi_profile: WiFiProfile) -> None:
        self.wifi_profiles.remove(wifi_profile)

        self._notify_observers("wifi_profiles_update")

    def get_wifi_profiles(self) -> List[WiFiProfile]:
        return self.wifi_profiles
    
    def select_wifi_profile(self, wifi_profile: WiFiProfile) -> None:
        if wifi_profile not in self.wifi_profiles:
            self.select_wifi_profile = self.wifi_profiles[0]
            self.logger.error("unknown wifi_profile selected")
        
        self.selected_wifi_profile = wifi_profile
        self._notify_observers("wifi_profile_selected")

    def get_wifi_profile_by_wifi_key(self, wifi_key: str) -> WiFiProfile:
        for wifi_profile in self.wifi_profiles:
            if wifi_profile.wifi_key == wifi_key:
                return wifi_profile
            
        return None

    def update_wifi_profile(self, updated_wifi_profile: WiFiProfile) -> None:
        for index, wifi_profile in enumerate(self.wifi_profiles):
            if updated_wifi_profile.wifi_key == wifi_profile.wifi_key:                
                self.wifi_profiles[index] = updated_wifi_profile
                break

        self._notify_observers("wifi_profiles_update")

    def add_microcontroller_capa(self, mcCapas: List[MicroControllerCapabilities]) -> None:
        for mcCapa in mcCapas:
            if mcCapa in self.mc_capabilities:
                continue
        
            self.mc_capabilities.append(mcCapa)

        self._notify_observers("microcontroller_capa_update")
    
    def remove_microcontroller_capa(self, mcCapa: MicroControllerCapabilities) -> None:
        self.mc_capabilities.remove(mcCapa)

        self._notify_observers("microcontroller_capa_update")

    def get_microcontroller_capas(self) -> List[MicroControllerCapabilities]:
        return self.mc_capabilities
    
    def select_microcontroller_capa(self, mcCapa: MicroControllerCapabilities) -> None:
        if mcCapa not in self.mc_capabilities:
            self.select_microcontroller = self.mc_capabilities[0]
            self.logger.error("unknown microcontroller capability selected")
        
        self.selected_mc_capability = mcCapa
        self._notify_observers("microcontroller_capa_selected")

    def get_microcontroller_capa_by_identity(self, identity: str) -> Optional[MicroControllerCapabilities]:
        for mcCapa in self.mc_capabilities:
            if mcCapa.identity == identity:
                return mcCapa
            
        return None
    
    def update_microcontroller_capa(self, mcCapa: MicroControllerCapabilities) -> None:
        for key, mc in enumerate(self.mc_capabilities):
            if mc.identity == mcCapa.identity:
                self.mc_capabilities[key] = mcCapa
                
                self._notify_observers("microcontroller_capa_update")

                break
        if self.selected_mc_capability and self.selected_mc_capability.identity == mcCapa.identity:
            self.selected_mc_capability = mcCapa
            self._notify_observers("microcontroller_capa_selected")

    def add_serial_port(self, serial_ports: List[SerialInfo]) -> None:
        self.serial_ports.clear()#to avoid doubles
        for serial_port in serial_ports:
            if serial_port in self.serial_ports:
                continue
        
            self.serial_ports.append(serial_port)
        
        self._notify_observers("serial_ports_update")

    def remove_serial_port(self, serial_port: SerialInfo) -> None:
        self.serial_ports.remove(serial_port)

        self._notify_observers("serial_ports_update")

    def get_serial_ports(self) -> List[SerialInfo]:
        return self.serial_ports
    
    def add_user(self, user: User) -> None:
        self.this_user.arduino_folder = user.arduino_folder

        self._notify_observers("user_update")

    def get_all_users(self) -> List[User]:
        return self.all_users
    
    def get_this_user(self) -> Optional[User]:
        return self.this_user
    
    def add_ble_address(self, ble_addresses: List[BLEInfo]) -> None:
        for ble_address in ble_addresses:
            if ble_address in self.ble_addresses:
                continue

            self.ble_addresses.append(ble_address)
        #TODO: check if we have doubles again
        self._notify_observers("ble_addresses_update")
    
    def remove_ble_address(self, ble_address: BLEInfo) -> None:
        self.ble_addresses.remove(ble_address)

        self._notify_observers("ble_addresses_update")

    def get_ble_addresses(self) -> List[BLEInfo]:
        return self.ble_addresses
    
    def get_ble_address_by_identity(self, mc_identity: str) -> Optional[BLEInfo]:
        for ble_address in self.ble_addresses:
            if ble_address.name == mc_identity:
                return ble_address
        
        return None
    
    def add_sensor_capabilities(self, mc_identity: str, sensor_capa: SensorCapabilities) -> None:
        raise NotImplementedError

    def remove_sensor_capability(self, mc_identity: str, sensor_capa: SensorCapabilities) -> None:
        raise NotImplementedError

    def get_sensor_capabilities(self, mc_identity: str) -> List[SensorCapabilities]:
        for mc_capa in self.mc_capabilities:
            if mc_capa.identity == mc_identity:
                return mc_capa.sensors
            
        return None
    
    def get_sensor_capability_by_identity(self, mc_identity: str, sensor_identity: str) -> Optional[SensorCapabilities]:
        for mc_capa in self.mc_capabilities:
            if mc_capa.identity == mc_identity:
                for sensor in mc_capa.sensors:
                    if sensor.identity == sensor_identity:
                        return sensor

        return None

    def update_sensor_capability(self, mc_identity: str, sensor_capa: SensorCapabilities) -> None:
        """
        this method replaces an old sensor capability by a new capability. be aware to include old capabilities that you are not updating so that we do not lose information.

        Args:
            mc_identity (str): the identity of the associated microcontroller
            sensor_capa (SensorCapabilities): the capabilities that want to be updated
        """
        for mc_capa in self.mc_capabilities:
            if mc_capa.identity == mc_identity:
                for key, sensor in enumerate(mc_capa.sensors):
                    if sensor.identity == sensor_capa.identity:
                        sensor[key] = sensor_capa
                        
                        self._notify_observers("microcontroller_capa_update")

                        break

    def add_actuator_capabilities(self, mc_identity: str, actuator_capa: ActuatorCapabilities) -> None:
        raise NotImplementedError

    def remove_actuator_capability(self, mc_identity: str, actuator_capa: ActuatorCapabilities) -> None:
        raise NotImplementedError
    
    def get_actuator_capabilities(self, mc_identity: str) -> List[ActuatorCapabilities]:
        for mc_capa in self.mc_capabilities:
            if mc_capa.identity == mc_identity:
                return mc_capa.actuators
            
        return None
    
    def get_actuator_capability_by_identity(self, mc_identity: str, actuator_identity: str) -> Optional[ActuatorCapabilities]:
        for mc_capa in self.mc_capabilities:
            if mc_capa.identity == mc_identity:
                for actuator in mc_capa.actuators:
                    if actuator.identity == actuator_identity:
                        return actuator

        return None
    
    def update_actuator_capability(self, mc_identity: str, actuator_capa: ActuatorCapabilities) -> None:
        """
        this method replaces an old actuator capability by a new capability. be aware to include old capabilities that you are not updating so that we do not lose information.

        Args:
            mc_identity (str): the identity of the associated microcontroller
            actuator_capa (ActuatorCapabilities): the capabilities that want to be updated
        """
        for mc_capa in self.mc_capabilities:
            if mc_capa.identity == mc_identity:
                for key, actuator in enumerate(mc_capa.actuators):
                    if actuator.identity == actuator_capa.identity:
                        actuator[key] = actuator_capa
                        
                        self._notify_observers("microcontroller_capa_update")

                        break

    def add_sensor_to_data_list(self, mc_identity: str, sensor_identity: str) -> None:
        """
        extend the _data object for additional microcontrollers and their associated sensors

        Args:
            mc_identity (str): the identity of a microcontroller
            sensor_identity (str): the identity of a sensor
        """
        if mc_identity not in self.data:
            self.data[mc_identity] = {}

        if sensor_identity not in self.data[mc_identity]:
            self.data[mc_identity][sensor_identity] = {}

        if "data" not in self.data[mc_identity][sensor_identity]:
            self.data[mc_identity][sensor_identity]["data"] = []

        if "last_accessed_index" not in self.data[mc_identity][sensor_identity]:
            self.data[mc_identity][sensor_identity]["last_accessed_index"] = -1

    def add_new_sensor_data(self, packet: Packet) -> None:
        """
        add new sensor data from the client to the model class

        this method retrieves microcontroller and sensor identity from header and payload, along with the payload itself. we convert the json to a dictionary and store it in self.data. we do NOT convert it to the associated modelclass because we do not know the model class while the sensor class does. and also, we can directly dump the dict to a file, whereas a datastructure with various model classes would be additional and unnessecary compute time.

        special attention to event_name:
        this is a unique key throughout the project which consists of the terms DATA, MC_IDENTITY and SENSOR_IDENTITY. this is used for this class to specifically call the sensor instance when new sensor data is available for it.

        Args:
            packet (Packet): packet that was sent from the network
        """
        mc_identity = packet.get_node_identity()
        json_data = packet.get_payload()
        data = json.loads(json_data)
        sensor_identity = data["identity"]
        event_name = f"DATA_{mc_identity}_{sensor_identity}"

        if mc_identity not in self.data:
            return
        
        if sensor_identity not in self.data[mc_identity]:
            return

        self.data[mc_identity][sensor_identity]["data"].append(data)
        
        self._notify_observers(event=event_name)

    def get_sensor_data(self, mc_identity: str, sensor_identity: str) -> List[Dict]:
        """
        this method is used to retrieve the latest sensor data, precisely cut to the sensor of a microcontroller
        """
        if mc_identity not in self.data or sensor_identity not in self.data[mc_identity]:
            # if the microcontroller or sensor identity does not exist, return an empty dict
            return []

        if "last_accessed_index" not in self.data[mc_identity][sensor_identity]:
            self.data[mc_identity][sensor_identity]["last_accessed_index"] = -1

        sensor_data = self.data[mc_identity][sensor_identity]
        last_accessed_index = sensor_data["last_accessed_index"]
        new_data = sensor_data["data"][last_accessed_index + 1:]

        if new_data:
            sensor_data["last_accessed_index"] = len(sensor_data["data"]) - 1

        return new_data
    
    def dump_all_sensor_data_to_json(self) -> None:
        all_data = {}

        for mc_identity, sensors in self.data.items():
            all_data[mc_identity] = {}
            for sensor_identity, sensor_info in sensors.items():
                all_data[mc_identity][sensor_identity] = sensor_info["data"]

        return json.dumps(all_data, indent=4)
