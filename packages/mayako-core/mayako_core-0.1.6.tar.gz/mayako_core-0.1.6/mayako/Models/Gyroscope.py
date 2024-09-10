from dataclasses import dataclass
from .BaseDataModel import BaseDataModel

@dataclass
class Gyroscope(BaseDataModel):
    x: float
    y: float
    z: float