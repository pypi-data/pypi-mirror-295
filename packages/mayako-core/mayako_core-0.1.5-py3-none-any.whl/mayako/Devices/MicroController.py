from typing import TypeVar, Type

from ..Utils.Identity import Identity
from ..Config import CERROR_MESSAGES, CCAPABILITIES, CCLIENT
from .Sensor import Sensor
from .Actuator import Actuator
from ..Models.MicrocontrollerCapabilities import MicroControllerCapabilities
from ..Command.CustomCommands import CustomCommands
from ..MayakoData import MayakoData
from ..Utils.Logger import LoggerInstance, LoggerType
from ..Models.BaseDataModel import BaseDataModel

T = TypeVar("T", bound=BaseDataModel) #for sensor model classes
S = TypeVar("S", bound=Actuator) #for actuator classes

class MicroController:

    _identity: str
    _logger: LoggerType

    def __init__(self, mc_identity: str, model: MayakoData, custom_commands: CustomCommands) -> None:
        Identity.register(identity=mc_identity)
        self._logger = LoggerInstance.get()
        self._identity = mc_identity #we store the identity for later reference although it is in capabilities
        self._model = model
        self._commands = custom_commands
        self._check_capabilities(self._identity)

    def _check_capabilities(self, mc_identity: str) -> None:
        """
        checks if the identity provided by the users matches a microcapa in mayakoData

        we do not store the capability here because we want the mayakoData be the single place which is responsible to manage this. also there might be a chance of corruption when the capabilities diverge.

        Args:
            identity (str): the identity of the microcontroller capability
        
        Raises:
            Exception: if no capa was found
        """
        capas = self._model.get_microcontroller_capa_by_identity(identity=mc_identity)
        if not capas:
            raise Exception(f"the microcontroller with the provided identity {self._identity} does not exist in {CCLIENT.CONFIG_FILE_NAME}. add a device with the identity in the mayakoGUI before defining the capabilities.")
        
    def get_capabilities(self) -> MicroControllerCapabilities:
        """retrieves the capabilities of this microcontroller"""
        return self._model.get_microcontroller_capa_by_identity(identity=self._identity)


    def define_capabilities(self, include_timestamp: bool = False, include_sequence: bool = False, delay: int = 0, duration: int = 0, max_samples: int = 0) -> None:
        """
        this method defines the capabilities for the microcontroller.

        first it loads the old capabilities from the microcontroller. then it constructs new capabilities with the information from the users. if the user information does not match with the old, the information in model is updated. pay attention: the old capabilities contain information such as wifi profile, sensors etc. that we want to keep. therefore if a missmatch is, just update the values. the capabilities are not directly updated on the device when the update on the model is performed but when the user executes client.start_record.

        Args:
            include_timestamp (bool): sensor data includes time stamp if true
            include_sequence (bool): sensor data includes a sequence number for each sensor individually
            delay (int): delays the execution of the record for x seconds after the start command was executed; unit seconds; is ignored if 0;
            duration (int): stops the record after x seconds; can be used together with stop command. whichever executes first, stops the record; unit is seconds; ignored if 0;
            max_samples (int): stops the record of x sensor data points were recorded; can run in parallel with duration and stop command; is ignoed if 0;
        """
        old_capas = self._model.get_microcontroller_capa_by_identity(self._identity)
        if not old_capas: #
            raise Exception(f"the microcontroller with the provided identity {self._identity} does not exist in {CCLIENT.CONFIG_FILE_NAME}. add a device with the identity in the mayako-gui before defining the capabilities.")
            
        new_capas = MicroControllerCapabilities(identity=self._identity, include_sequence=include_sequence, include_timestamp=include_timestamp, delay=delay, duration=duration, max_samples=max_samples)

        if not self._compare_capabilities(old_capa=old_capas, new_capa=new_capas):
            #we must update the capabilities
            self._logger.debug("updating microcontroller capabilities")
            #we may only update the changing things!!! the old capa contains infos we still need
            self._update_old_capabilities(old_capa=old_capas, new_capa=new_capas)
            self._model.update_microcontroller_capa(old_capas)
        else:
            self._logger.debug("no update on microcontroller capabilities")

    def _compare_capabilities(self, old_capa: MicroControllerCapabilities, new_capa: MicroControllerCapabilities) -> bool:
        """compares if the microcontroller capabilities match"""
        return (
        old_capa.include_sequence == new_capa.include_sequence and
        old_capa.include_timestamp == new_capa.include_timestamp and
        old_capa.delay == new_capa.delay and
        old_capa.duration == new_capa.duration and
        old_capa.max_samples == new_capa.max_samples
    )

    def _update_old_capabilities(self, old_capa: MicroControllerCapabilities, new_capa: MicroControllerCapabilities) -> None:
        """assign changes from the new microcontroller capability to the old"""
        old_capa.include_sequence = new_capa.include_sequence
        old_capa.include_timestamp = new_capa.include_timestamp
        old_capa.delay = new_capa.delay
        old_capa.duration = new_capa.duration
        old_capa.max_samples = new_capa.max_samples

    def use_sensor(self, sensor_class_type: Type[T], sensor_identity: str) -> Sensor[T]:
        """
        creates a sensor that wants to retrieve sensor data with the type from sensor_class_type

        Args:
            sensor_class_type (Type[T]): a sensor data model class
            sensor_identity (str): identity of a sensor

        Returns:
            Sensor[T]: returns a sensor that 
        """
        sens_capa = self._model.get_sensor_capability_by_identity(self._identity, sensor_identity)
        if not sens_capa:
            raise Exception(f"the sensor with the provided identity {sensor_identity} does not exist in {CCLIENT.CONFIG_FILE_NAME}.")
        
        return Sensor[T](sensor_identity=sensor_identity, mc_identity=self._identity, model=self._model, sensor_class_type=sensor_class_type)

    def use_actuator(self, class_type: Type[S], actuator_identity: str) -> S:
        """
        creates an actuator that can execute commands associated with it

        Args:
            class_type (Type[S]): the specific actuator class which is a subclass of Actuator
            actuator_identity (str): the identity of the actuator

        Return:
            Type[S]: an instance of an actuator implementation which is a sublcass of Actuator
        """
        if not issubclass(class_type, Actuator):
            raise TypeError(f"{class_type.__name__} is not a subclass of {Actuator.__name__}")
        
        act_capa = self._model.get_actuator_capability_by_identity(self._identity, actuator_identity)
        if not act_capa:
            raise Exception(f"the actuator with the provided identity {actuator_identity} does not exist in {CCLIENT.CONFIG_FILE_NAME}.")
        
        return class_type(identity=actuator_identity, mc_identity=self._identity, model=self._model, commands=self._commands)
    
    def get_identity(self) -> str:
        """returns the identity of this microcontroller"""
        return self._identity