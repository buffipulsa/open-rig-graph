
from dataclasses import dataclass

from .transform import Transform


@dataclass(frozen=True)
class Entity:
    id: str
    parent_id: str | None
    local_transform: Transform