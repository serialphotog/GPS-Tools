from dataclasses import dataclass
from typing import Optional


@dataclass
class GPSPoint:
    name: Optional[str]
    latitude: float
    longitude: float
    description: Optional[str]
