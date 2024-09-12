from dataclasses import dataclass

from krri_common.models.train_direction import TrainDirection


@dataclass(frozen=True)
class TrainSummary:
    """
    used at occupation description for memory optimization
    """
    position: int
    direction: TrainDirection
