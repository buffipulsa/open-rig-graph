
from .entity import Entity
from .transform import Transform, compose_transform


def evaluate_world_transform(
    entity_id: str,
    entities: dict[str, Entity]
) -> Transform:
    
    entity = entities[entity_id]
    
    if entity.parent_id is None:
        return entity.local_transform
    
    parent_world = evaluate_world_transform(entity.parent_id, entities)
    
    return compose_transform(parent_world, entity.local_transform)