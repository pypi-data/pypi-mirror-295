import struct
from crc import Calculator, Configuration

from ..Config import CPACKET, CERROR_MESSAGES
from ..Utils.Logger import LoggerType, LoggerInstance

class Packet:
    """
    This module deserialises binary data received with an implemented protocol while also serialising data for network transfer. It provides functionality to split the header from the payload, performs checksum test and also verifies if a byte contains the flag for a mayakoProtocol packet.

    The structure of the binary packet is described in protocol_interface.md

    Do not access the members of the class directly, use the getter and setter functions to avoid unexpected behaviour.

    Sources:
        https://docs.python.org/3/library/struct.html
        https://pypi.org/project/crc/

    Attributes:
        _method : int (8bit)
            makes the first byte of each packet and the header. indicates the purpose of the packet in the mayako framework. can be one of 6 hexademical values which can be found in config.py
        _node_identity : int (32 bit)
            contains the name of the microcontroller or the client application which sent the packet. Node identity is a fixed-size 4 byte ASCII integer so that it can be integrated in the binary header. This lets everyone directly recognise the source of the packet and requires no further identification inside the payload. The node identity for each microcontroller and client application must be unique throughout the project and (probably) also in BLE/WiFi range. The node identity for the microcontroller is defined with the upload of a new build and can not changed for commands. 
        _sequence : int (16 bit)
            there is a difference between _sequence in the packet and sequence in the payload of sensor data. _sequence works across generic packets and tracks the order of the  packets. It is intended to work with ACK packets. the microcontroller app uses a 16 bit unsigned integer for _sequence, therefore we must be cautious and can only use _sequence until 2¹⁶-1.
        _checksum : int (8 bit)
            we use CRC to calculate the checksum of the payload to ensure the integrity of the data. corrupted or incomplete data fails to test the checksum which should trigger a ACK packet with a retry request. the parameters for the CRC calculation can be found in protocol_interface.md.
        _payload_size : int (16 bit)
            to ensure that we can savely read the content of each packet, besides starting with the method flag, we integrated a payload size 2 byte field in the header on position 9 and 10. this contains the length of the payload and helps the protocols to read data until the end. therefore we do not have to rely on a newline character and can read/write binary data.
        _payload : bytes
            payload is of variable size and is encoded to utf-8 using JSON format. the size is sent in the header. more on the structure of payload can be read in protocol_interface.md.
            NYI: currently only text encoding is available. change encoding based on data (video data, audio data, etc.). we recommend an additional header field which indicates that encoding that has to be updated in the network protocol specification.
        _header_size : int (10 byte)
            the header size is an integral part of the packet and has a fix size of 10 bytes. this must be uniformly enforced across all implementation. failure to comply may result in unexpected behaviour, communication errors and data misinterpretations. Following th header, the payload has variable size only limited by the MTU of the implemented protocol. the header size is not integrated into the header because of its constant nature.
        _packet_size: int (variable)
            the sum of _header_size and _payload_size

    Todo:
        * encoding field in the header
    """
    _logger: LoggerType
    _method: int
    _node_identity: int
    _sequence: int
    _checksum: int
    _payload_size: int
    _payload: bytes
    _header_size: int
    _packet_size: int

    def __init__(self) -> None:
        """
        set all members to None. incorrect usage results in members still being None.
        """
        self._logger = LoggerInstance.get()
        self._method = None
        self._node_identity = None
        self._sequence = 0
        self._checksum = None
        self._payload_size = None
        self._payload = None
        self._header_size = CPACKET.HEADER_SIZE
        self._packet_size = None

    def set_method(self, method: int) -> None:
        """
        sets _method. best use the constants from Config.py as argument.
        
        Args:
            method (int): the argument must be a 1 byte hex value

        Returns:
            None
        """

        self._method = method

    def set_node_identity(self, node_identity: str) -> None:
        """
        node_identity is a 4 byte long name. this function does not validate if it is a 4 byte ASCII string. node identity is passed as a string that is then converted to bytes with ascii encoding.

        Args:
            node_identity (str): 4 byte string that can be encoded to ASCII

        Returns:
            None
        """
        if len(node_identity) != CPACKET.NODE_IDENTITY_LENGTH:
            raise ValueError(CERROR_MESSAGES.NODE_IDENTITY_LENGTH)

        self._node_identity = int.from_bytes(node_identity.encode(CPACKET.HEADER_ENCODING))

    def _set_sequence(self, sequence: int) -> None:
        """
        sequence is a 2 byte number. it is automatically managed by the Integrity Manager is may not be set manually otherwise resulting in unexpected behaviour and maybe congestion issues.

        Args:
            sequence (int): sequence indicates the order of packets on the network

        Returns:
            None
        """
        self._sequence = sequence

    def _set_checksum(self, checksum: int) -> None:
        """
        checksum is a 8 bit number. it is automatically managed. do not set this manually otherwise unexpected behaviour may occur.

        Args:
            checksum (int): 8 bit CRC checksum

        Returns:
            None
        """
        self._checksum = checksum

    def _set_payload_size(self, payload_size: int) -> None:
        """
        payload_size is an 16 bit number. it is automatically managed. do not set this manually otherwise unexpected behaviour may occur.

        Args:
            payload_size (int): size of the payload

        Returns:
            None
        """
        self._payload_size = payload_size

    def set_payload(self, payload: str) -> None:
        """
        the payload is first encoded to uft-8. We calculate the payloadsize and the checksum from it.

        Args:
            payload (str): a JSON string with commands, data, or error messages

        Returns:
            None
        """
        self._payload = payload.encode(CPACKET.PAYLOAD_ENCODING)
        self._payload_size  = len(self._payload)
        self._checksum = self.calculate_checksum(self._payload)

    def get_method(self) -> int:
        """
        Returns the method.

        Args:
            None

        Returns:
            _method (int) 8 bit integer
        """
        return self._method
    
    def get_node_identity(self) -> str:
        """
        Returns the node identity.

        Args:
            None

        Returns:
            _node_identity (str) identity of the microcontroller or client application which sent the packet
        """
        return self._node_identity.to_bytes(4).decode(CPACKET.HEADER_ENCODING)
    
    def get_sequence(self) -> int:
        """
        Returns the sequence.

        Args:
            None

        Returns:
            _sequence (int)
        """
        return self._sequence
    
    def get_checksum(self) -> int:
        """
        Returns the checksum
        
        Args:
            None

        Returns:
            _checksum (int) 8 bit CRC checksum
        """
        return self._checksum
    
    def get_payload_size(self) -> int:
        """
        Returns the payload size

        Args:
            None

        Returns:
            _payload_size (int)
        """
        return self._payload_size
    
    def get_payload(self) -> str:
        """
        Returns the payload.

        Args:
            None

        Returns:
            _payload (str)
        """
        
        return self._payload.decode(CPACKET.PAYLOAD_ENCODING)
    
    def get_packet_size(self) -> int:
        """
        Returns the packet size.

        Args:
            None

        Returns:
            packet size (int)
        """
        return self._packet_size
    
    def serialize(self) -> bytes:
        """
        Before using serialise method, node_identity, and payload must have been set. Raises an exception if one or more are None. packet size is calculated from header and payload size. this is used to compare with the MTU of the implemented procotol before sending over the network, probably encountering errors or corrupted data. the header is built with the package struct. the 10 byte header is formated with format characters that can be found in config.py. it packs method, node_identity, sequence, checksum and payload. it results in a byte array. header is then combined with the byte array of the payload to complete a ready to send packet.

        Source:
            #https://docs.python.org/3/library/struct.html

        Args:
            None

        Returns:
            packet (bytes): the packet contains header and payload an can be sent over the network like this

        Raises:
            ValueError: if _method, _node_identity, or _payload are not set (None) before calling seriliase.

        """
        if self._method == None or self._node_identity == None or self._payload == None:
            raise ValueError(CERROR_MESSAGES.PACKET_NOT_SET)


        self._packet_size = self._header_size +  self._payload_size
        
        header = struct.pack(CPACKET.HEADER_FORMAT_CHARACTERS, self._method, self._node_identity, self._sequence, self._checksum, self._payload_size)

        return header + self._payload
    
    def deserialize_header(self, buffer: bytes) -> bool:
        """
        the deserialise method is split into two functions. this is due to the fact how we are reading the data in the implemented protocol read function. first we check if the buffer has enough data for the header, deserialise it, and result with a payload size. because we are reading binary data and do not rely on a stop character such as new line, we require the payload size from byte 9 and 10 before being able to read the payload.

        in this function we first unpack the 10 byte bytes array with the struct packet with a defined character format. this results in a tuple (length 5) which contains method, node_identity, sequence, checksum and payload_size. these are not returned but stored in the class as properties which should be later read with getter methods as needed. do use both deserialise methods before using getter methods.

        Args:
            buffer (bytes): the byte buffer read from the network starting with the method flag

        Returns:
            anonymous (boolean): if buffer is not HEADER_SIZE it returns false
        """
        if len(buffer) == CPACKET.HEADER_SIZE - 1:
            return False
        
        result: tuple = struct.unpack(CPACKET.HEADER_FORMAT_CHARACTERS, buffer)
        
        self._method = result[0]
        self._node_identity = result[1]
        self._sequence = result[2]
        self._checksum = result[3]
        self._payload_size = result[4]

        return True
    
    def deserialize_payload(self, buffer: bytes) -> bool:
        """
        deserialises the payload. this sets the payload as a byte array. use getter method to get the decoded paylaod.

        Args:
            buffer (bytes): the payload of a packet
        
        Returns:
            anonymous (boolean): if the buffer is not the payload_size it returns false
        """
        if len(buffer) < self._payload_size:
            self._logger.debug(len(buffer))
            self._logger.debug(self._payload_size)
            return False
        
        self._payload = buffer

        return True

    @staticmethod
    def calculate_checksum(payload: bytes) -> int:
        """
        static method to calcuate the CRC checksum

        Args:
            payload (bytes)

        Returns:
            checksum (int): 8 bit CRC checksum
        """
        crc_config = Configuration(width=CPACKET.CRC_WIDTH,
                                   polynomial=CPACKET.CRC_POLYNOMIAL,
                                   init_value=CPACKET.CRC_INIT_VALUE,
                                   final_xor_value=CPACKET.CRC_FINAL_XOR_VALUE, reverse_input=CPACKET.CRC_REVERSE_INPUT,
                                   reverse_output=CPACKET.CRC_REVERSE_OUTPUT)

        calculator = Calculator(configuration=crc_config)

        return calculator.checksum(payload)
    
    def verify_checksum(self) -> bool:
        """
        verifies the checksum with the properties of packet. used after deserialising the packet.

        Args:
            None

        Returns:
            anonymous (boolean): if the checksum of the checksum from the header and performing the checksum on the payload inplace match
        """
        if self._payload == None or self._checksum == None:
            raise ValueError(CERROR_MESSAGES.PACKET_NOT_SET)

        return self.calculate_checksum(self._payload) == self._checksum
    
    @staticmethod
    def verify_flag(flag: bytes) -> bool:
        """
        static method to verify a one byte integer. compares with the method flags of the mayakoProtocol. if it matches, this indicates that the passed flag is the first byte of a packet from this protocol. the flag may not be an integer so we try to convert it.

        Args:
            flag (bytes): one byte of data

        Returns:
            anonymous (boolean): if the flag is from the mayakoProtocol packet
        """
        if type(flag) != int:
            flag = int.from_bytes(flag)

        if flag == CPACKET.METHOD_ACKNOWLEDGEMENT:
            return True
        elif flag == CPACKET.METHOD_DATA:
            return True
        elif flag == CPACKET.METHOD_COMMAND:
            return True
        elif flag == CPACKET.METHOD_HEARTBEAT:
            return True
        elif flag == CPACKET.METHOD_DEBUG:
            return True
        elif flag == CPACKET.METHOD_INFO:
            return True
        elif flag == CPACKET.METHOD_ERROR:
            return True
        else:
            return False
        
    def verify_good_packet(self) -> bool:
        """
        this method is a combination of verify flag and perform checksum. requires a packet to be deserialised. Do not call before deserialising.

        Args:
            None

        Returns: 
            anonymous (boolean) if verify flag and checksum passed
        """
        
        return self.verify_flag(self.get_method()) and self.verify_checksum()