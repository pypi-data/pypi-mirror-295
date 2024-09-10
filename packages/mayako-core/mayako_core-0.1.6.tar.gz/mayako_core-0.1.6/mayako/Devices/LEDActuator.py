from ..MayakoData import MayakoData
from ..Command.CustomCommands import CustomCommands
from .Actuator import Actuator

class LEDActuator(Actuator):

    def __init__(self, identity: str, mc_identity: str, model: MayakoData, commands: CustomCommands) -> None:
        super().__init__(identity, mc_identity, model, commands)

    def switch_on(self, index: int, red: int, green: int, blue: int) -> None:
        parameters = {
            "index": index,
            "red": red,
            "green": green,
            "blue": blue
        }
        self._commands.execute(self._mc_identity, "SWITCH_ON", parameters)

    def switch_off(self) -> None:
        self._commands.execute(self._mc_identity, "SWITCH_OFF")