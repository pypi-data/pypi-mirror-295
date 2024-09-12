import base64
import io
from datetime import datetime

from matplotlib import pyplot as plt
from msgspec import Struct
from msgspec.json import encode, decode


class Spectrogram(Struct):
    start_time: datetime
    time_range: int
    image: bytes
    block_index: int
    block_unit_size: int
    distance_rate: float
    start_offset: int
    end_offset: int
    position_offset: int

    @classmethod
    def create(cls, start_time: datetime, time_range: int, image: plt, block_index: int, block_unit_size: int,
               distance_rate: float, start_offset: int, end_offset: int, position_offset: int):
        bio = io.BytesIO()
        image.savefig(bio, format='jpg', dpi=72)
        bio.seek(0)
        image_bytes = bio.read()
        return cls(start_time=start_time, time_range=time_range, image=image_bytes, block_index=block_index,
                   block_unit_size=block_unit_size, distance_rate=distance_rate,
                   start_offset=start_offset, end_offset=end_offset, position_offset=position_offset)

    @classmethod
    def from_json(cls, json):
        return decode(json, type=Spectrogram)

    def to_json(self):
        return encode(self)
