#this is the contrast to LEDActuator. it handles custom execution mode while providing nearly not syntax highlighting
from mayako.MayakoData import MayakoData
from .Actuator import Actuator


class CustomActuator(Actuator):

    def __init__(self, identity: str, model: MayakoData) -> None:
        super().__init__(identity, model)

    def execute(self, cmd_name: str, parameters: dict = {}) -> None:
        #add mc_id
        #add id
        #self.commands.execute(mc_id, act_id, cmd_name)
        pass