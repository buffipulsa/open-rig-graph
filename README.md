# OpenRigGraph

OpenRigGraph is an application-independent representation and runtime for
procedural character rigs and animation.

## Current experiment

The project currently begins with a deliberately small three-transform FK
chain:

```text
root -> mid -> end
```

The current semantic model contains immutable entities. Each entity has:

- a stable string identifier;
- an optional parent identifier;
- a local `Transform`.

`Transform` is an immutable value containing:

- translation as an `(x, y, z)` tuple;
- rotation as an `(x, y, z, w)` quaternion tuple;
- scale as an `(x, y, z)` tuple.

The pure `compose_transform(parent, local)` operation derives a child world
transform from a parent world transform and a local transform. The current
composition model uses component-wise scale multiplication, quaternion
rotation composition, and parent-space transformation of the local
translation. It does not represent shear.

The evaluator derives world transforms through the entity hierarchy:

- `evaluate_world_transform` evaluates one entity;
- `evaluate_world_transforms` evaluates every entity;
- cycles raise `ValueError`;
- missing entities and parents raise `KeyError`.

The experiment intentionally does not yet include animation, serialization,
plugins, generalized graph infrastructure, optimization, or DCC integration.

## Development setup

The project uses `uv` and a `src/` package layout. Start a Python session
with:

```powershell
uv run python
```

Run the complete FK example:

```python
from open_rig_graph.entity import Entity
from open_rig_graph.evaluation import evaluate_world_transforms
from open_rig_graph.transform import Transform

entities = {
    "root": Entity(
        id="root",
        parent_id=None,
        local_transform=Transform(translation=(10.0, 0.0, 0.0)),
    ),
    "mid": Entity(
        id="mid",
        parent_id="root",
        local_transform=Transform(translation=(2.0, 0.0, 0.0)),
    ),
    "end": Entity(
        id="end",
        parent_id="mid",
        local_transform=Transform(translation=(3.0, 0.0, 0.0)),
    ),
}

world_transforms = evaluate_world_transforms(entities)

for entity_id, transform in world_transforms.items():
    print(entity_id, transform)
```

The expected world translations are:

```text
root -> (10.0, 0.0, 0.0)
mid  -> (12.0, 0.0, 0.0)
end  -> (15.0, 0.0, 0.0)
```

The repository intentionally keeps this first experiment independent of Maya
and other DCC applications.
