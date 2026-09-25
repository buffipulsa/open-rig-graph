# OpenRigGraph

OpenRigGraph is an application-independent representation and runtime for
procedural character rigs and animation.

## Current experiment

The project currently begins with a deliberately small three-transform FK
experiment. A transform is an immutable value containing:

- translation as an `(x, y, z)` tuple;
- rotation as an `(x, y, z, w)` quaternion tuple;
- scale as an `(x, y, z)` tuple.

`compose_transform(parent, local)` derives a child world transform from a
parent world transform and a local transform. The current composition model
uses component-wise scale multiplication, quaternion rotation composition,
and parent-space transformation of the local translation. It does not yet
include entities, hierarchy evaluation, animation, serialization, plugins,
or DCC integration.

## Development setup

The project uses `uv` and a `src/` package layout. Run the current experiment
with:

```powershell
uv run python
```

Then import the transform value and composition function:

```python
from open_rig_graph.transform import Transform, compose_transform

parent = Transform(translation=(10.0, 0.0, 0.0))
local = Transform(translation=(2.0, 0.0, 0.0))

print(compose_transform(parent, local))
```

The repository intentionally keeps the first experiment independent of Maya
and other DCC applications.
