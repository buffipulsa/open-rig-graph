
from .entity import Entity
from .transform import Transform, compose_transform


def evaluate_world_transform(
    entity_id: str,
    entities: dict[str, Entity]
) -> Transform:
    
    return _evaluate_world_transform(
        entity_id=entity_id,
        entities=entities,
        visiting=set()
    )

def evaluate_world_transforms(
    entities: dict[str, Entity]
) -> dict[str, Transform]:
    
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