from ..Utils.Identity import Identity
from ..MayakoData import MayakoData
from ..Utils.Logger import LoggerInstance, LoggerType

class Device:

    _identity: str
    _mc_identity: str
    _model: MayakoData
    _logger: LoggerType

    def __init__(self, identity: str, mc_identity: str, model: MayakoData) -> None:
        Identity.register(identity)
        self._identity = identity
        self._mc_identity = mc_identity
        self._model = model
        self._logger = LoggerInstance.get()

    def get_identity(self) -> str:
        """returns the identity of the actuator or sensor"""
        return self._identity