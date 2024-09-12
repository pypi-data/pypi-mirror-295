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

    @classmethod
    def create(cls, start_time: datetime, time_range: int, image: plt):
        bio = io.BytesIO()
        image.savefig(bio, format='png')
        bio.seek(0)
        image_bytes = base64.b64decode(bio.read())
        return cls(start_time=start_time, time_range=time_range, image=image_bytes)

    @classmethod
    def from_json(cls, json):
        return decode(json, type=Spectrogram)

    def to_json(self):
        return encode(self)
