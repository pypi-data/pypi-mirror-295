from dataclasses import dataclass
from .BaseDataModel import BaseDataModel

@dataclass
class Heartrate(BaseDataModel):
    heartrate: float
    sp02: int