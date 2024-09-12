import dataclasses
from datetime import datetime
from typing import List

from msgspec import Struct
from msgspec.json import decode, encode


@dataclasses.dataclass
class PreparedPhaseMessageItem:
	initial_time: datetime
	offset: int


class PreparedPhaseMessage(Struct):
	contents: List[PreparedPhaseMessageItem]

	@classmethod
	def from_json(cls, json):
		return decode(json, type=PreparedPhaseMessage)

	def to_json(self) -> bytes:
		return encode(self)
