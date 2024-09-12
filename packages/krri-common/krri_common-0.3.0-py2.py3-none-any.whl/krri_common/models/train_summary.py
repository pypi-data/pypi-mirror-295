from dataclasses import dataclass

from krri_common.models.train_direction import TrainDirection
from msgspec import Struct
from msgspec.json import decode, encode


class TrainSummary(Struct):
    """
    used at occupation description for memory optimization
    """
    position: int
    direction: TrainDirection

    @classmethod
    def from_json(cls, json):
        decoded_data = decode(json)
        position = decoded_data['position']
        direction = decoded_data['direction']
        return cls(position=position, direction=TrainDirection(direction))

    def to_json(self) -> str:
        return encode(self)
