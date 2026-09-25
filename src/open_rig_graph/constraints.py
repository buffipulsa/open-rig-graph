
from dataclasses import dataclass

@dataclass(frozen=True)
class AimConstraint:
    driven_id: str
    target_id: str
    up_direction: tuple[float, float, float] = (0.0, 0.0, 1.0)#