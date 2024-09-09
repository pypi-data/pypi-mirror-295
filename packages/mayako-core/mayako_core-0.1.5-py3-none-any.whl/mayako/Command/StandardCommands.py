from queue import Queue
from typing import Dict
import json

from ..Config import CCOMMAND, CPACKET
from ..Models.MicrocontrollerCapabilities import MicroControllerCapabilities
from ..Models.WiFiProfile import WiFiProfile
from ..Network.Packet import Packet

class StandardCommands:
    """
    this is the class for the standard commands which are defined in protocol_interface.md

    it is not meant to be directly used by the user. each function creates a Packet instance which holds the mc_identity (the destination of the packet), the command method, and the payload. the packet instance is stored in the queue of the client which is frequently flushed to the network.
    """

    def __init__(self, client_queue: Queue[Packet]) -> None:
        self._client_queue = client_queue

    def _make_packet(self, mc_identity:str, doc: Dict) -> None:
        """
        this is a helper function which creates a packet from the dictionary.

        Args:
            mc_identity (str): identity of a microcontroller
            doc (Dict): the payload of the packet in dictionary format

        :
            Packet:  a ready-to-send packet
        """
        jsonDoc = json.dumps(doc)

        packet = Packet()
        packet.set_method(CPACKET.METHOD_COMMAND)
        packet.set_node_identity(mc_identity)
        packet.set_payload(jsonDoc)
        
        self._client_queue.put(packet)

    def record_create(self, mc_identity: str, capabilities: MicroControllerCapabilities) -> None:
        """
        this method creates a packet from the provided model class and the identity of the microcontroller

        mc_identity is used so that we know where to send the packet to (mapping mc <-> network address). use packet.get_node_identity() to get the identity. adding cmd_name to the dictionary created with to_dict() and serialise as json string. the packet is created with the method which is fix COMMAND, the identity (microcontroller) and the payload which is the json string. this packet can directly be sent. we want the payload to be flat because this makes it easier on the mayako-node and we only have to add cmd_name (only keyword in the payload). also most of the time we dont have a payload. adding a parameters property would only bloat the payload.

        Args:
            mc_identity (str): identity of the microcontroller that is the target of the packet
            capabilities(MicroControllerCapabilities): capabilities of a certain microcotrnoller

        :
            Packet: a packet class that contains all information for a network implementation to send it to the micrcontroller
        """
        #mc/node identiy so that we know where this packet should be aimed at
        doc = capabilities.to_dict()
        doc["cmd_name"] = CCOMMAND.RECORD_CREATE
        
        self._make_packet(mc_identity, doc)
    
    def record_start(self, mc_identity: str) -> None:
        """
        this command start the record on the mayako-node if it is not already running

        Args:
            mc_identity (str): identity of the microcontroller

        :
            Packet: command wrapped in packet class
        """
        doc = {}
        doc["cmd_name"] = CCOMMAND.RECORD_START

        self._make_packet(mc_identity, doc)

    def record_stop(self, mc_identity: str) -> None:
        """
        this command stops the record on the mayako-node if it is running

        Args:
            mc_identity (str): identity of the microcontroller

        :
            Packet: command wrapped in packet class
        """
        doc = {}
        doc["cmd_name"] = CCOMMAND.RECORD_STOP

        self._make_packet(mc_identity, doc)

    def record_read(self, mc_identity: str) -> None:
        """
        this command reads the capabilities of the mayako-node

        Args:
            mc_identity (str): identity of the microcontroller

        :
            Packet: command wrapped in packet class
        """
        doc = {}
        doc["cmd_name"] = CCOMMAND.RECORD_READ

        self._make_packet(mc_identity, doc)

    def restart(self, mc_identity: str) -> None:
        """
        this command restarts the mayako-node

        Args:
            mc_identity (str): identity of the microcontroller

        :
            Packet: command wrapped in packet class
        """
        doc = {}
        doc["cmd_name"] = CCOMMAND.RESTART

        self._make_packet(mc_identity, doc)

    def battery_read(self, mc_identity: str) -> None:
        """
        this command reads the battery of the mayako-node

        Args:
            mc_identity (str): identity of the microcontroller

        :
            Packet: command wrapped in packet class
        """
        doc = {}
        doc["cmd_name"] = CCOMMAND.BATTERY_READ

        self._make_packet(mc_identity, doc)

    def identify(self, mc_identity: str, identity: str) -> None:
        """
        this command start the record on the mayako-node if it is not already running

        Args:
            mc_identity (str): identity of the microcontroller
            identity (str): this is the identity of the microcontroller/sensor/actuator which should be identified.

        :
            Packet: command wrapped in packet class
        """
        doc = {}
        doc["cmd_name"] = CCOMMAND.IDENTIFY
        doc["identity"] = identity

        self._make_packet(mc_identity, doc)

    def connection_read(self, mc_identity: str) -> None:
        """
        this command reads the connection status and the protocol used

        Args:
            mc_identity (str): identity of the microcontroller

        :
            Packet: command wrapped in packet class
        """
        doc = {}
        doc["cmd_name"] = CCOMMAND.CONNECTION_READ

        self._make_packet(mc_identity, doc)

    def wifi_profile_create(self, mc_identity: str, wifi_profile: WiFiProfile) -> None:
        """
        this command creates a new wifi profile on the mayako-node

        Args:
            mc_identity (str): identity of the microcontroller

        :
            Packet: command wrapped in packet class
        """
        doc = wifi_profile.to_dict()
        doc["cmd_name"] = CCOMMAND.WIFI_PROFILE_CREATE

        self._make_packet(mc_identity, doc)

    def wifi_profile_read(self, mc_identity: str, wifi_key: str) -> None:
        """
        this command read a wifi profile by wifi_key

        Args:
            mc_identity (str): identity of the microcontroller
            wifi_key (str): identity of a wifi profile

        :
            Packet: command wrapped in packet class
        """
        doc = {}
        doc["cmd_name"] = CCOMMAND.WIFI_PROFILE_READ
        doc["wifi_key"] = wifi_key

        self._make_packet(mc_identity, doc)

    def wifi_profile_active_read(self, mc_identity: str) -> None:
        """
        this command reads the wifi profile that is marked as the active wifi profile. the active wifi profile is the profile that is loaded on start.

        Args:
            mc_identity (str): identity of the microcontroller

        :
            Packet: command wrapped in packet class
        """
        doc = {}
        doc["cmd_name"] = CCOMMAND.WIFI_PROFILE_ACTIVE_READ

        self._make_packet(mc_identity, doc)

    def wifi_profile_all_read(self, mc_identity: str) -> None:
        """
        this command reads all wifi profiles on the mayako-node

        Args:
            mc_identity (str): identity of the microcontroller

        :
            Packet: command wrapped in packet class
        """
        doc = {}
        doc["cmd_name"] = CCOMMAND.WIFI_PROFILE_ALL_READ

        self._make_packet(mc_identity, doc)

    def wifi_profile_active_select(self, mc_identity: str, wifi_key: str) -> None:
        """
        this command changes the wifi profile to a wifi profile that is stored on the mayako-node using the according wifi-key

        Args:
            mc_identity (str): identity of the microcontroller
            wifi_key (str): the wifi_key of the wifi profile on the mayako-node that we want to select as the active wifi profile

        :
            Packet: command wrapped in packet class
        """
        doc = {}
        doc["cmd_name"] = CCOMMAND.WIFI_PROFILE_ACTIVE_SELECT
        doc["wifi_key"] = wifi_key

        self._make_packet(mc_identity, doc)

    def wifi_profile_delete(self, mc_identity: str) -> None:
        """
        this command reads all wifi profiles on the mayako-node

        Args:
            mc_identity (str): identity of the microcontroller

        :
            Packet: command wrapped in packet class
        """
        doc = {}
        doc["cmd_name"] = CCOMMAND.WIFI_PROFILE_DELETE

        self._make_packet(mc_identity, doc)


