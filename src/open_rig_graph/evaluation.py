
"""Evaluate world transforms from a semantic entity hierarchy."""

from .entity import Entity
from .transform import Transform, compose_transform


def evaluate_world_transform(
    entity_id: str,
    entities: dict[str, Entity]
) -> Transform:
    """Evaluate one entity's world transform through its parent chain.

    Parameters
    ----------
    entity_id : str
        Stable identity of the entity to evaluate.
    entities : dict[str, Entity]
        Semantic entities indexed by stable identity.

    Returns
    -------
    Transform
        The derived world transform of the requested entity.

    Raises
    ------
    KeyError
        If the requested entity or one of its parents is missing.
    ValueError
        If the parent relationships contain a cycle.
    """
    
    return _evaluate_world_transform(
        entity_id=entity_id,
        entities=entities,
        visiting=set()
    )

def evaluate_world_transforms(
    entities: dict[str, Entity]
) -> dict[str, Transform]:
    """Evaluate the world transform of every entity.

    Parameters
    ----------
    entities : dict[str, Entity]
        Semantic entities indexed by stable identity.

    Returns
    -------
    dict[str, Transform]
        Derived world transforms indexed by entity identity.

    Raises
    ------
    KeyError
        If an entity or one of its parents is missing.
    ValueError
        If the parent relationships contain a cycle.
    """
    
    return {
        entity_id: evaluate_world_transform(
            entity_id=entity_id,
            entities=entities
        ) for entity_id in entities
    }
    
def _evaluate_world_transform(
    entity_id: str,
    entities: dict[str, Entity],
    visiting: set[str]
) -> Transform:
    """Recursively evaluate one entity while tracking the active path.

    Parameters
    ----------
    entity_id : str
        Stable identity of the entity to evaluate.
    entities : dict[str, Entity]
        Semantic entities indexed by stable identity.
    visiting : set[str]
        Entity identities currently being evaluated on the recursion path.

    Returns
    -------
    Transform
        The derived world transform of the requested entity.

    Raises
    ------
    KeyError
        If the entity or its parent is missing.
    ValueError
        If the current parent path contains a cycle.
    """
    
    if entity_id in visiting:
        raise ValueError(
            f'Hierarchy cycle detected at entity {entity_id!r}.'
        )
    
    try:
        entity = entities[entity_id]
    except KeyError as error:
        raise KeyError(
            f'Unknown entity {entity_id!r}.'
        ) from error
    
    visiting.add(entity_id)
    
    try:
        if entity.parent_id is None:
            return entity.local_transform
        
        if entity.parent_id not in entities:
            raise KeyError(
                f'Entity {entity_id!r} references missing parent '
                f'{entity.parent_id!r}.'
            )
            
        parent_world = _evaluate_world_transform(
            entity.parent_id,
            entities,
            visiting
        )
        
        return compose_transform(parent_world, entity.local_transform)
    finally:
        visiting.remove(entity_id)
