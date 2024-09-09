from abc import ABC
from dataclasses import dataclass, asdict
from typing import Self, Dict, Optional

@dataclass
class BaseDataModel(ABC):
    """
    this is the base class for all model classes that are related to sensor data from the microcontrollers such as Accelerometer or Heartratesensor. Creating new model classes requires inheriting this class.

    Sources:
        https://www.arduino.cc/reference/en/language/functions/time/millis/

    Attributes:
        identity (str): the unique identity within a microcontroller that indicates the sensor
        timestamp (Optional[int]): a timestamp when the data point was created; pay attention that arduino boards use millis() function which returns the milliseconds passed from starting the arduino board, not unix time; is optional; default is None
        sequence (Optional[int]): the sequence of data points since the record started; is optional; default is None

    Source
        https://stackoverflow.com/a/2544761
    """
    identity: str
    timestamp: Optional[int]
    sequence: Optional[int]

    def to_dict(self, filter_none=True) -> dict:
        """
        Makes a dictionary from the model class.

        Args:
            filter_none (bool):
                all None values are excluded from the conversion

        Returns:
            Dict: a dictionary representation of this instance
        """
        data = asdict(self)

        if filter_none:
            return {key: value for key, value in data.items() if value is not None}
        
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> Self:
        """
        Creates a model instance from dictionary.

        this method creates an instance of the according model class using information from a dictionary. as the values timestamp and sequence may not be included, a default value is set to None.

        Sources:
            https://stackoverflow.com/a/3483652

        Returns:
            (Self): returns an instance of the model class
        """
        data.setdefault("timestamp", None)
        data.setdefault("sequence", None)
        
        return cls(**data)
    
    def get_class_name(self) -> str:
        """
        returns the name of the model class
        """
        return self.__class__.__name__