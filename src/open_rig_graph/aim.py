
"""Pure aim-direction and aim-constraint evaluation."""

import numpy as np
from numpy.typing import NDArray

from .constraints import AimConstraint
from .entity import Entity
from .transform import Transform, to_local_rotation


def compute_aim_rotation(
    source_position: tuple[float, float, float],
    target_position: tuple[float, float, float],
    up_direction: tuple[float, float, float]
) -> tuple[float, float, float, float]:
    """Compute a rotation that aims the local +X axis at a target.

    Parameters
    ----------
    source_position : tuple[float, float, float]
        Position of the driven object.
    target_position : tuple[float, float, float]
        Position the driven object should aim toward.
    up_direction : tuple[float, float, float]
        Direction used to resolve the local +Y axis.

    Returns
    -------
    tuple[float, float, float, float]
        A unit quaternion in ``(x, y, z, w)`` order.

    Raises
    ------
    ValueError
        If the source and target coincide, the up direction is zero-length,
        or the up direction is parallel to the aim direction.
    """
    
    source: NDArray[np.float64] = np.asarray(
        source_position,
        dtype=float
    )
    target: NDArray[np.float64] = np.asarray(
        target_position,
        dtype=float
    )
    up: NDArray[np.float64] = np.asarray(
        up_direction,
        dtype=float
    )
    
    aim = target - source
    aim_length = np.linalg.norm(aim)
    
    if np.isclose(aim_length, 0.0):
        raise ValueError(
            'Cannot aim at a target located at the source position.'
        )
        
    aim /= aim_length
    
    up_length: float = np.linalg.norm(up)
    
    if np.isclose(up_length, 0.0):
        raise ValueError(
            'Up direction cannot be zero-length.'
        )
    
    up /= up_length
    
    alignment: float = float(np.dot(up, aim))
    projected_up: NDArray[np.float64] = up - alignment * aim
    projected_up_length = np.linalg.norm(projected_up)
    
    if np.isclose(projected_up_length, 0.0):
        raise ValueError(
            'Up direction cannot be parallel to the aim direction.'
        )
        
    y_axis = projected_up / projected_up_length
    z_axis = np.cross(aim, y_axis)
    
    basis: NDArray[np.float64] = np.column_stack(
        (aim, y_axis, z_axis)
    )
    
    return _quaternion_from_basis(basis=basis)

def apply_aim_rotation(
    transform: Transform,
    target_position: tuple[float, float, float],
    up_direction: tuple[float, float, float]
) -> Transform:
    """Apply an aim rotation while preserving translation and scale.

    Parameters
    ----------
    transform : Transform
        Transform whose translation provides the source position.
    target_position : tuple[float, float, float]
        Position the transform should aim toward.
    up_direction : tuple[float, float, float]
        Direction used to resolve the driven orientation's up axis.

    Returns
    -------
    Transform
        A transform with the computed rotation and the original translation
        and scale.
    """
    
    rotation = compute_aim_rotation(
        source_position=transform.translation,
        target_position=target_position,
        up_direction=up_direction
    )
    
    return Transform(
        translation=transform.translation,
        rotation=rotation,
        scale=transform.scale
    )

def apply_aim_rotation_in_parent_space(
    local_transform: Transform,
    source_world_position: tuple[float, float, float],
    target_world_position: tuple[float, float, float],
    parent_world_rotation: tuple[float, float, float, float],
    up_direction: tuple[float, float, float]
) -> Transform:
    """Apply a world-space aim and return the result in parent space.

    Parameters
    ----------
    local_transform : Transform
        Original transform authored relative to the parent.
    source_world_position : tuple[float, float, float]
        Driven position in world space.
    target_world_position : tuple[float, float, float]
        Target position in world space.
    parent_world_rotation : tuple[float, float, float, float]
        Parent's world-space rotation.
    up_direction : tuple[float, float, float]
        Direction used to resolve the driven orientation's up axis.

    Returns
    -------
    Transform
        A local transform with the constrained rotation and original
        translation and scale.
    """
    
    world_rotation = compute_aim_rotation(
        source_position=source_world_position,
        target_position=target_world_position,
        up_direction=up_direction
    )
    
    local_rotation = to_local_rotation(
        parent_rotation=parent_world_rotation,
        world_rotation=world_rotation
    )
    
    return Transform(
        translation=local_transform.translation,
        rotation=local_rotation,
        scale=local_transform.scale
    )

def evaluate_aim_constraint_in_parent_space(
    constraint: AimConstraint,
    entities: dict[str, Entity],
    world_transforms: dict[str, Transform]
) -> Transform:
    
    try:
        driven_entity = entities[constraint.driven_id]
    except KeyError as error:
        raise KeyError(
            f'Unknown driven entity {constraint.driven_id!r}.'
        ) from error
        
    try:
        driven_world = world_transforms[constraint.driven_id]
    except KeyError as error:
        raise KeyError(
            'Missing world transform for driven entity '
            f'{constraint.driven_id!r}.'
        ) from error
        
    try:
        target_world = world_transforms[constraint.target_id]
    except KeyError as error:
        raise KeyError(
            f'Unknown target entity {constraint.target_id!r}.'
        ) from error
        
    if driven_entity.parent_id is None:
        parent_world_rotation = (0.0,0.0,0.0,1.0)
    else:
        try:
            parent_world_rotation = world_transforms[
                driven_entity.parent_id
            ].rotation
        except KeyError as error:
            raise KeyError(
                'Missing world transform for parent '
                f'{driven_entity.parent_id!r}.'
            ) from error
            
    return apply_aim_rotation_in_parent_space(
        local_transform=driven_entity.local_transform,
        source_world_position=driven_world.translation,
        target_world_position=target_world.translation,
        parent_world_rotation=parent_world_rotation,
        up_direction=constraint.up_direction
    )

def evaluate_aim_constraints(
    constraint: AimConstraint,
    world_transforms: dict[str, Transform]
) -> Transform:
    """Evaluate one semantic aim constraint from world transforms.

    Parameters
    ----------
    constraint : AimConstraint
        Semantic relationship to evaluate.
    world_transforms : dict[str, Transform]
        Derived world transforms indexed by stable entity identity.

    Returns
    -------
    Transform
        The constrained driven world transform.

    Raises
    ------
    KeyError
        If the driven or target entity is absent from ``world_transforms``.
    """
    
    try:
        driven_transform = world_transforms[constraint.driven_id]
    except KeyError as error:
        raise KeyError(
            f'Unknown driven entity {constraint.driven_id!r}.'
        ) from error
        
    try:
        target_transform = world_transforms[constraint.target_id]
    except KeyError as error:
        raise KeyError(
            f'Unknown target entity {constraint.target_id!r}.'
        ) from error

    return apply_aim_rotation(
        transform=driven_transform,
        target_position=target_transform.translation,
        up_direction=constraint.up_direction
    )

def _quaternion_from_basis(
    basis: NDArray[np.float64]
) -> tuple[float, float, float, float]:
    """Convert an orthonormal basis matrix to a unit quaternion.

    Parameters
    ----------
    basis : NDArray[np.float64]
        Three-by-three rotation basis with the aim, up, and side axes as
        columns.

    Returns
    -------
    tuple[float, float, float, float]
        Unit quaternion in ``(x, y, z, w)`` order.
    """
    
    matrix00 = basis[0, 0]
    matrix01 = basis[0, 1]
    matrix02 = basis[0, 2]
    matrix10 = basis[1, 0]
    matrix11 = basis[1, 1]
    matrix12 = basis[1, 2]
    matrix20 = basis[2, 0]
    matrix21 = basis[2, 1]
    matrix22 = basis[2, 2]
    
    trace = matrix00 + matrix11 + matrix22
    
    if trace > 0.0:
        scale = np.sqrt(trace + 1.0) * 2.0
        quaternion = (
            (matrix21 - matrix12) / scale,
            (matrix02 - matrix20) / scale,
            (matrix10 - matrix01) / scale,
            0.25 * scale
        )
    elif matrix00 > matrix11 and matrix00 > matrix22:
        scale = np.sqrt(1.0 + matrix00 - matrix11 - matrix22) * 2.0
        quaternion = (
            0.25 * scale,
            (matrix01 + matrix10) / scale,
            (matrix02 + matrix20) / scale,
            (matrix21 - matrix12) / scale,
        )
    elif matrix11 > matrix22:
        scale = np.sqrt(1.0 + matrix11 - matrix00 - matrix22) * 2.0
        quaternion = (
            (matrix01 + matrix10) / scale,
            0.25 * scale,
            (matrix12 + matrix21) / scale,
            (matrix02 - matrix20) / scale
        )
    else:
        scale = np.sqrt(1.0 + matrix22 - matrix00 - matrix11) * 2.0
        quaternion = (
            (matrix02 + matrix20) / scale,
            (matrix12 + matrix21) / scale,
            0.25 * scale,
            (matrix10 - matrix01) / scale
        )
        
    return (
        float(quaternion[0]),
        float(quaternion[1]),
        float(quaternion[2]),
        float(quaternion[3]),
    )



