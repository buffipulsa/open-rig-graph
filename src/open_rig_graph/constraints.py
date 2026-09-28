
"""Semantic constraint definitions."""

from dataclasses import dataclass


@dataclass(frozen=True)
class AimConstraint:
    """Describe an aim relationship between two semantic entities.

    Attributes
    ----------
    driven_id : str
        Stable identity of the entity whose rotation is constrained.
    target_id : str
        Stable identity of the entity being aimed at.
    up_direction : tuple[float, float, float]
        Direction used to resolve the driven orientation's up axis.

    Notes
    -----
    The current world-space aim evaluator interprets ``up_direction`` in
    world space.
    """

    driven_id: str
    target_id: str
    up_direction: tuple[float, float, float] = (0.0, 0.0, 1.0)
