
import numpy as np

from .transform import Transform

def compute_aim_rotation(
    source_position: tuple[float, float, float],
    target_position: tuple[float, float, float],
    up_direction: tuple[float, float, float]
) -> tuple[float, float, float, float]:
    
    source = np.asarray(source_position, dtype=float)
    target = np.asarray(target_position, dtype=float)
    up = np.asarray(up_direction, dtype=float)
    
    aim = target - source
    aim_length = np.linalg.norm(aim)
    
    if np.isclose(aim_length, 0.0):
        raise ValueError(
            'Cannot aim at a target located at the source position.'
        )
        
    aim /= aim_length
    
    up_length = np.linalg.norm(up)
    
    if np.isclose(up_length, 0.0):
        raise ValueError(
            'Up direction cannot be zero-length.'
        )
    
    up /= up_length
    
    projected_up = up - np.dot(up, aim) * aim
    projected_up_length = np.linalg.norm(projected_up)
    
    if np.isclose(projected_up_length, 0.0):
        raise ValueError(
            'Up direction cannot be parallel to the aim direction.'
        )
        
    y_axis = projected_up / projected_up_length
    z_axis = np.cross(aim, y_axis)
    
    basis = np.column_stack((aim, y_axis, z_axis))
    
    return _quaternion_from_basis(basis=basis)

def apply_aim_rotation(
    transform: Transform,
    target_position: tuple[float, float, float],
    up_direction: tuple[float, float, float]
):
    
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

def _quaternion_from_basis(
    basis: np.ndarray
) -> tuple[float, float, float, float]:
    
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
        
    return tuple(float(component) for component in quaternion)