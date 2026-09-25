
"""Semantic entities used to describe a rig hierarchy."""

from dataclasses import dataclass

from .transform import Transform


@dataclass(frozen=True)
class Entity:
    """A stable transform entity in the semantic rig definition.

    Attributes
    ----------
    id : str
        Stable identity used to reference the entity.
    parent_id : str or None
        Stable identity of the structural parent, or ``None`` for a root.
    local_transform : Transform
        Transform authored relative to the entity's parent.

    Notes
    -----
    The entity stores only its local transform. A world transform is derived
    during evaluation and is not persistent entity state.
    """

    id: str
    parent_id: str | None
    local_transform: Transform
