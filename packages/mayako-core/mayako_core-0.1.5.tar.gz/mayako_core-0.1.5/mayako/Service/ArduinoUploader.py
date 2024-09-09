import os, importlib, subprocess, uuid
from ..Models.WiFiProfile import WiFiProfile
from ..Network.NetworkInterface import NetworkProtocols
from ..Utils.Logger import LoggerInstance, LoggerType
from ..Config import CGENERAL, CNETWORK

class ArduinoUploader:

    """
    References:
        https://docs.platformio.org/en/latest/projectconf/sections/env/options/build/build_flags.html
    """

    PACKAGE_NAME = "platformio"
    PIO_CONFIG_FILE = "platformio.ini"

    def __init__(self, arduino_path: str, identity: str, serial_port: str, wireless_mode: NetworkProtocols = NetworkProtocols.BLE, wifi_profile: WiFiProfile = None) -> None:
        self.logger: LoggerType = LoggerInstance.get()
        self.arduino_path = arduino_path #relative path
        self.project_path = os.path.join(os.getcwd(), self.arduino_path)
        self.identity = identity
        self.service_uuid = uuid.uuid4()
        self.characteristic_uuid = uuid.uuid4()
        self.serial_port = serial_port
        self.wireless_mode = wireless_mode
        self.wifi_profile = wifi_profile
    
    def check_prerequisits(self) -> bool:
        if not os.path.exists(self.project_path):
            self.logger.error(f"path to arduino directory does not exist")
            return False
        
        #check if the platformio CLI exists and can be used
        try:
            importlib.import_module(self.PACKAGE_NAME)
                    
        except ImportError as e:
            self.logger.error(e)
            return False
        
        #check if platformio.ini data exists in the current working directory. this is a good indicator for a folder with a arduino build to upload.
        pioini_path = os.path.join(self.project_path, self.PIO_CONFIG_FILE)

        if not os.path.exists(pioini_path):
            self.logger.error(f"pioini_path {pioini_path} does not exist")
            return False

        #check if identity is an ascii string and 4 byte long
        if not self.identity.isascii():
            self.logger.error(f"{self.identity} is not of ASCII type")
            return False
        
        if len(self.identity) != 4:
            self.logger.error(f"{self.identity} must be 4 byte long")
            return False

        return True
    
    def _create_flag(self) -> str:
        flags = [
            f'-DMC_NAME=\\"{self.identity}\\"',
            f'-DSERVICE_UUID=\\"{self.service_uuid}\\"',
            f'-DCHARACTERISTIC_UUID=\\"{self.characteristic_uuid}\\"',
            f'-DPORT=\\"{self.serial_port}\\"',
            f'-DBAUDRATE={CNETWORK.BAUDRATE}',
            f'-DDEBUG_MODE={CGENERAL.DEBUG}'
        ]

        if self.wireless_mode == NetworkProtocols.BLE:
            flags.append('-DWIRELESS_MODE=0')
        else:
            flags.extend([
                '-DWIRELESS_MODE=1',
                f'-DSSID=\\"{self.wifi_profile.ssid}\\"',
                f'-DPASSWORD=\\"{self.wifi_profile.password}\\"',
                f'-DCLIENT_IP=\\"{self.wifi_profile.client_ip}\\"',
                f'-DCLIENT_PORT=\\"{self.wifi_profile.client_port}\\"'
            ])

        return flags
    
    def upload(self) -> bool:

        os.environ['PLATFORMIO_BUILD_FLAGS'] = ' '.join(self._create_flag())

        command = [
            self.PACKAGE_NAME, 'run', '-t', 'upload', '--upload-port', self.serial_port, '--project-dir', self.project_path
        ]
             
        try:
            process = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)
            self.logger.error(process.stderr)

            return process.returncode == 0
        except subprocess.CalledProcessError as e:
            self.logger.error(f"upload failed: {e}")
        
        except FileNotFoundError as e:
            self.logger.error(f"command unknown: {e}")

        return False

    
if __name__ == "__main__":
    #upload a build with wifi enabled; ble requires a different build     
    wifi_profile = WiFiProfile(
        wifi_key="WIFI_PROFILE_2",
        ssid="172.168.192.0",
        password="1829746238267463950124",
        client_ip="172.168.192.27",
        client_port=8001
    )

    a = ArduinoUploader("./arduino", "MC01", "/dev/ttyUSB0", NetworkProtocols.WIFI, wifi_profile)
    if a.check_prerequisits(): a.upload()

    #alternative with BLE
    a = ArduinoUploader("./arduino", "MC01", "/dev/ttyUSB0", NetworkProtocols.BLE)
    if a.check_prerequisits(): a.upload()