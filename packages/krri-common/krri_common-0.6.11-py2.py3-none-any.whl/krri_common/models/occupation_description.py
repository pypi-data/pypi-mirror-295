from datetime import datetime
from typing import List

import numpy as np
from msgspec import Struct
from msgspec.json import decode, encode
from nptyping import NDArray, Shape, Int32

from krri_common.models.train_summary import TrainSummary


class OccupationDescription(Struct):
    measurement_time: datetime
    time_unit_per_data: float
    _occupation_map: List
    group_of_train_position_summaries: List[TrainSummary]

    @property
    def occupation_map(self):
        return np.array(self._occupation_map)

    def to_json(self) -> bytes:
        return encode(self)

    @classmethod
    def from_json(cls, json):
        return decode(json, type=OccupationDescription)

    @classmethod
    def create(cls, measurement_time: datetime, time_unit_per_data: float,
               occupation_map: NDArray[Shape['"*", "*"'], Int32],
               group_of_train_position_summaries: List[TrainSummary]):
        return cls(measurement_time=measurement_time, time_unit_per_data=time_unit_per_data,
                   _occupation_map=getattr(occupation_map, "tolist", lambda: value)(),
                   group_of_train_position_summaries=group_of_train_position_summaries)
