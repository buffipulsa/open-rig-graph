
"""Application-independent transform values and composition.

This module contains the first small evaluation primitive for OpenRigGraph:
an immutable TRS transform value and pure parent/local transform composition.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Transform:
    """An immutable translation, rotation, and scale value.

    Attributes
    ----------
    translation : tuple[float, float, float]
        Translation in the value's current coordinate space.
    rotation : tuple[float, float, float, float]
        Unit quaternion in ``(x, y, z, w)`` order.
    scale : tuple[float, float, float]
        Component-wise scale in the value's current coordinate space.
    """

    translation: tuple[float, float, float] = (0.0,0.0,0.0)
    rotation: tuple[float, float, float, float] = (0.0,0.0,0.0,1.0)
    scale: tuple[float, float, float] = (1.0,1.0,1.0)
    
def compose_transform(
    parent: Transform,
    local: Transform,
) -> Transform:
    """Compose a local transform with a parent transform.

    Parameters
    ----------
    parent : Transform
        The parent transform, normally in world space.
    local : Transform
        The child transform relative to the parent.

    Returns
    -------
    Transform
        The composed child transform in the parent's space.

    Notes
    -----
    This implementation assumes unit quaternion rotations and uses
    component-wise scale multiplication without representing shear.
    """
    
    parent_scale = parent.scale
    local_translation = local.translation
    
    scaled_translation = tuple(
        parent_scale[index] * local_translation[index]
        for index in range(3)
    )
    
    rotated_translation = _rotate_vector(
        parent.rotation,
        scaled_translation,
    )
    
    world_translation = tuple(
        parent.translation[index] + rotated_translation[index]
        for index in range(3)
    )
    
    world_rotation = _quaternion_multiply(
        parent.rotation,
        local.rotation
    )
    
    world_scale = tuple(
        parent.scale[index] * local.scale[index]
        for index in range(3)
    )
    
    return Transform(
        translation=world_translation,
        rotation=world_rotation,
        scale=world_scale
    )
    
def _quaternion_multiply(
    first: tuple[float, float, float, float],
    second: tuple[float, float, float, float]
) -> tuple[float, float, float, float]:
    """Multiply two quaternions in ``(x, y, z, w)`` order."""
    
    first_x, first_y, first_z, first_w = first
    second_x, second_y, second_z, second_w = second
    
    return (
        first_w * second_x
        + first_x * second_w
        + first_y * second_z
        - first_z * second_y,
        first_w * second_y
        - first_x * second_z
        + first_y * second_w
        + first_z * second_x,
        first_w * second_z
        + first_x * second_y
        - first_y * second_x
        + first_z * second_w,
        first_w * second_w
        - first_x * second_x
        - first_y * second_y
        - first_z * second_z,
    )
    
def _rotate_vector(
    rotation: tuple[float, float, float, float],
    vector: tuple[float, float, float]
) -> tuple[float, float, float]:
    """Rotate a vector by a unit quaternion."""
    
    qx, qy, qz, qw = rotation
    vx, vy, vz = vector
    
    tx = 2.0 * (qy * vz - qz * vy)
    ty = 2.0 * (qz * vx - qx * vz)
    tz = 2.0 * (qx * vy - qy * vx)
    
    return (
        vx + qw * tx + qy * tz - qz * ty,
        vy + qw * ty + qz * tx - qx * tz,
        vz + qw * tz + qx * ty - qy * tx,
    )
    
