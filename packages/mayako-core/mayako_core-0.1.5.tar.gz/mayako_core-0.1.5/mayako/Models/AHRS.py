from dataclasses import dataclass
from .BaseDataModel import BaseDataModel

@dataclass
class AHRS(BaseDataModel):
    pitch: float
    roll: float
    yaw: float