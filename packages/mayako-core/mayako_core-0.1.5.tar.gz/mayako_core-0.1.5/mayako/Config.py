class CERROR_MESSAGES:
    DESCRIPTION_WRONG_TYPE: str = "description must be of type string"
    ALL_ARGUMENTS_MICROCONTROLLER: str = "all arguments must be of type Microcontroller"
    ALL_ARGUMENTS_DEVICE: str = "all arguments must be of type Device"
    ITEM_ALREADY_EXISTS_IN_DICT: str = "Key already exists in dictionary: "
    CLASS_NO_INIT: str = "This class should not be instantiated."
    PACKET_NOT_SET: str = "method, node_identity or payload are None. set these properties before calling serialise."
    NODE_IDENTITY_LENGTH: str = "a node identity must be 4 characters long"
    TYPE_MUST_BE_LIST: str = "the argument must be of type list"
    TYPE_MUST_BE_CALLABLE: str = "callback must be of type function"

class CCOMMAND:
    RECORD_CREATE: str = "RECORD_CREATE"
    RECORD_START: str = "RECORD_START"
    RECORD_STOP: str = "RECORD_STOP"
    RECORD_READ: str = "RECORD_READ"
    
    RESTART: str = "RESTART"
    BATTERY_READ: str = "BATTERY_READ"
    IDENTIFY: str = "IDENTIFY"

    CONNECTION_READ: str = "CONNECTION_READ"
    WIFI_PROFILE_CREATE: str = "WIFI_PROFILE_CREATE"
    WIFI_PROFILE_READ: str = "WIFI_PROFILE_READ"
    WIFI_PROFILE_ACTIVE_READ: str = "WIFI_PROFILE_ACTIVE_READ"
    WIFI_PROFILE_ALL_READ: str = "WIFI_PROFILE_ALL_READ"
    WIFI_PROFILE_ACTIVE_SELECT: str = "WIFI_PROFILE_SELECT"
    WIFI_PROFILE_DELETE: str = "WIFI_PROFILE_DELETE"

#custom commands are transfered with RECORD_READ

class CFEEDBACK:
    RECORD_INFO: str = "RECORD_INFO"
    BATTERY_INFO: str = "BATTERY_INFO"
    IDENTIFY_INFO: str = "IDENTIFY_INFO"
    WIFI_INFO: str = "WIFI_INFO"
    WIFI_PROFILE_INFO: str = "WIFI_PROFILE_INFO"
    PROTOCOL_INFO: str = "PROTOCOL_INFO"
    CAPABILITIES_INFO: str = "CAPABILITIES_INFO"

class CNETWORK:
    SERIAL_NAME: str = "SERIAL"
    WIFI_NAME: str = "WIFI"
    BLE_NAME: str = "BLE"
    OUT_OF_ORDER_PACKET_MAX_SIZE: int = 5
    SEQUENCE_MAX_NUMBER_SIZE: int = 65535 #2¹⁶-1 unsigned
    SEND_ACK_PACKETS: bool = True
    HEARTBEAT_INTERVALint = 1000 #ms
    BAUDRATE: int = 115200
    TIMEOUT = 1
    BUFFER_SIZE = 1000
    SERIAL_ARDUINO_WORDS = ["Arduino", "CP2104"] #add more words if necessary to find other boards
    SELECTED_PATHS = ["platformio.ini", "lib", "src"]
    BUSY_WAITING_TIMEOUT = 0.001
    PORT_ALREADY_USED_CODE = 98

class CPACKET:
    HEADER_SIZE: int = 10
    HEADER_PAYLOADSIZE_POSITION: int = 8 #plus 9 because payload takes 2 bytes
    #reserve the 6 characters in ASCII table starting with 0x20 and ending with 0x26 as the beginning byte of our packets
    METHOD_ACKNOWLEDGEMENT: int = 0x20 #SP #32
    METHOD_DATA: int = 0x21 #! #33
    METHOD_COMMAND: int = 0x22 #" #34
    METHOD_HEARTBEAT: int = 0x23 ## #35
    METHOD_DEBUG: int = 0x24 #$ #36
    METHOD_INFO: int = 0x25 #% #37
    METHOD_ERROR: int = 0x26 #& 38
    HEADER_ENCODING: str = "ascii"
    PAYLOAD_ENCODING: str = "utf-8"
    HEADER_FORMAT_CHARACTERS: str = "!BIHBH"
    NODE_IDENTITY_LENGTH: int = 4

    CRC_WIDTH: int = 8
    CRC_POLYNOMIAL: int = 0xa7
    CRC_INIT_VALUE: int = 0x00
    CRC_FINAL_XOR_VALUE: int = 0x00
    CRC_REVERSE_INPUT: bool = True
    CRC_REVERSE_OUTPUT: bool = True

class CCAPABILITIES:
    DEFAULT_DURATION: int = 0#milli seconds
    DEFAULT_MAX_SAMPLES: int = 0
    DEFAULT_DELAY: int = 0#milli seconds
    DEFAULT_INCLUDE_SEQUENCE: bool = False
    DEFAULT_INCLUDE_TIMESTAMP: bool = False
    DEFAULT_INCLUDE_SENSOR: bool = False
    DEFAULT_INCLUDE_ACTUATOR: bool = False
    DEFAULT_SAMPLE_RATE: int = 250
    DEFAULT_DATA_ON_CHANGE: bool = False

class CCLIENT:
    PORT = 7777
    CONFIG_FILE_NAME = "mayako.json"
    DEFAULT_ARDUINO_FOLDER = "arduino"

class CGENERAL:
    DEBUG = 1