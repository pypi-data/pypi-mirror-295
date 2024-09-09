from .Device import Device
from ..MayakoData import MayakoData
from ..Models.ActuatorCapabilities import ActuatorCapabilities
from ..Command.CustomCommands import CustomCommands
from ..Config import CCLIENT

class Actuator(Device):

    def __init__(self, identity: str, mc_identity: str, model: MayakoData, commands: CustomCommands) -> None:
       super().__init__(identity=identity, mc_identity=mc_identity, model=model)
       self._commands = commands
       self._check_capabilities(self._identity)

    def define_capabilities(self, enable: bool = True) -> None:
        """
        this function lets the user change capabilties of the actuator subclass

        Args:
            enable (bool): if the actuator is enabled or not
        """
        old_capas = self._check_capabilities(actuator_identity=self._identity)

        new_capas = ActuatorCapabilities(identity=self._identity, enable=enable)

        if not self._compare_actuator_capabilities(old_capas=old_capas, new_capas=new_capas):
            self._logger.debug("updating actuator capability")
            self._model.update_actuator_capability(self._mc_identity, new_capas)
        else:
            self._logger.debug("no update on actuator capability")

    def _check_capabilities(self, actuator_identity: str) -> ActuatorCapabilities:
        """checks if there is a capability associated with the acutator identity"""
        capas = self._model.get_actuator_capability_by_identity(mc_identity=self._mc_identity, actuator_identity=actuator_identity)
        if not capas:
            raise Exception(f"the actuator with the provided identity {actuator_identity} does not exist in {CCLIENT.CONFIG_FILE_NAME}.")
        
        return capas

    def get_capabilities(self) -> ActuatorCapabilities:
        """returns the capabilities of the actuator"""
        return self._model.get_actuator_capability_by_identity(self._identity)

    def _compare_actuator_capabilities(self, old_capas: ActuatorCapabilities, new_capas: ActuatorCapabilities) -> bool:
        """compares the actuator capabilities"""
        return (
            old_capas.enable == new_capas.enable
        )