# Chapter 04 — Reconstructing a ModelPart from MDPA

An MDPA file is a serialized ModelPart: it names registered entity types, supplies connectivity and IDs, and records group membership and initial data. Reading one correctly requires the same ownership and variable rules used when constructing a ModelPart in Python.

## Run the example

```bash
python3 tutorial/04_mdpa_io/read_mdpa.py
```

## MDPA is an object-graph description

The example file is [case/triangle.mdpa](case/triangle.mdpa). Its key blocks are:

| Block | Meaning |
|---|---|
| `ModelPartData` | Values placed in root `ProcessInfo`, such as `DOMAIN_SIZE` |
| `Table` | Sampled mapping between registered variables |
| `Properties <id>` | Shared typed values referenced by elements/conditions |
| `Nodes` | `id x y z` coordinates |
| `Elements <registered_name>` | `id property_id node_ids...` |
| `Conditions <registered_name>` | `id property_id node_ids...` |
| `NodalData <variable>` | `node_id is_fixed value` initial/prescribed historical values |
| `ElementalData` / `ConditionalData` | Non-historical values on entities |
| `SubModelPart` | Named hierarchical membership lists |

Whitespace is flexible, but block names, registered component names, IDs, and value types matter.

## Correct read order

The reader cannot invent application components or historical storage. Read a model in this order:

1. import Kratos core;
2. import every Application needed by element, condition, law, or variable names;
3. create `Model` and the destination root `ModelPart`;
4. add historical nodal variables that the MDPA contains or the solver needs;
5. invoke `ModelPartIO`;
6. add DOFs or let the application solver add them (a fixed `NodalData` entry also creates/fixes its DOF while reading);
7. run checks before solving.

The path passed to `ModelPartIO` conventionally omits `.mdpa`:

```python
KM.ModelPartIO("path/to/triangle").ReadModelPart(model_part)
```

The example builds the absolute stem from `__file__`, making it independent of the shell's working directory.

## `NodalData` fixity field

For scalar data:

```text
Begin NodalData TEMPERATURE
    1  0  100.0
End NodalData
```

The middle field is fixity: `0` stores the value without fixing its DOF; `1` creates/fixes the corresponding DOF while reading. Prefer process-defined boundary conditions in reusable cases because processes can support intervals, expressions, tables, and clearer semantic grouping. MDPA fixity remains useful for simple or generated models.

## SubModelParts are membership, not copies

The `HotBoundary` block lists node and condition IDs already defined at root. On read, Kratos reconstructs views referencing those entities. A process later addresses the group as `Main.HotBoundary`.

A reliable preprocessor should include every node required by each listed element/condition and produce semantically named groups. Names such as `HotBoundary`, `Supports`, and `FluidDomain` are more maintainable than GUI-generated labels when you control the pipeline.

## Mesh versus material versus run settings

A clean full case separates responsibilities:

- **MDPA:** coordinates, connectivity, property IDs, initial entity data, groups;
- **Materials JSON:** property values and constitutive-law choices;
- **ProjectParameters JSON:** solver, time, processes, output, and filenames;
- **Python entry point:** constructs the Model and AnalysisStage, then runs it.

Kratos also supports other import/modeler routes and can write ModelParts. MDPA remains valuable because it is inspectable, deterministic, and widely supported in Kratos workflows.

## Common failures

- Passing a path with an accidental `.mdpa.mdpa` suffix.
- Reading `NodalData` for a historical variable that was not added first.
- Using a physics element name before importing its Application.
- Mismatched node count for an entity type.
- Referencing a nonexistent property or node ID.
- Defining a 2D mesh but leaving `DOMAIN_SIZE` unset or inconsistent.
- Applying a process to `Main.SomeGroup` when the group exists under another root name.

## Work through these changes

1. Add a fourth node and second triangle directly in the MDPA; verify total area in Python.
2. Add a `ColdBoundary` submodelpart containing node 2.
3. Change the `TEMPERATURE` fixity field for node 1 to `1`, then inspect `HasDofFor` and `IsFixed` after reading.
4. Write the loaded ModelPart to a new MDPA with `ModelPartIO(..., KM.IO.WRITE)` and compare its semantics, not formatting.
5. Deliberately misspell `Element2D3N`, read the registration error, and formulate a diagnostic checklist.

Next: [Chapter 05 — Elements and global equations](../05_elements_and_linear_systems/README.md).
