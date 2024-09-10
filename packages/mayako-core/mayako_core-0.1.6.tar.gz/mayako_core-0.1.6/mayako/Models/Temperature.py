from dataclasses import dataclass
from .BaseDataModel import BaseDataModel

@dataclass
class Temperature(BaseDataModel):
    temperature: float
