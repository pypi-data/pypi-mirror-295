from queue import Queue
import json
from typing import Dict

from ..Network.Packet import Packet
from ..Config import CPACKET

class CustomCommands:
    """
    this custom class contains an interface for users to execute custom commands for actuators on the mayako-nodes. directly using this might expose risks, we recommend implementing an actuator class. it uses the clients queue to store packet. these are frequently flushed to the network by the client. the client injects an instance of this class into actuator, which lets it use by the client in a subclass of actuator.
    """

    def __init__(self, client_queue: Queue[Packet]) -> None:
        self._client_queue = client_queue

    def execute(self, mc_identity: str, cmd_name: str, parameters: Dict = {}) -> None:
        doc = parameters
        doc["cmd_name"] = cmd_name

        jsonDoc = json.dumps(doc)

        packet = Packet()
        packet.set_method(CPACKET.METHOD_COMMAND)
        packet.set_node_identity(mc_identity)
        packet.set_payload(jsonDoc)
        
        self._client_queue.put(packet)