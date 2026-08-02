# Chapter 01 — The Model, ModelParts, and mesh entities

Every Kratos analysis is built around a `Model` and one or more `ModelPart` objects. Before dealing with solvers, be precise about what these containers own, what a SubModelPart represents, and how mesh entities refer to one another. This object graph explains many input and boundary-condition errors.

## Run the example

```bash
python3 tutorial/01_model_and_modelparts/model_and_modelparts.py
```

## `Model`: the top-level index

A simulation normally owns one `Model`:

```python
model = KM.Model()
domain = model.CreateModelPart("Domain")
```

The model provides name-based access to root and nested model parts:

```python
model["Domain"]
model["Domain.Boundary.Inlet"]
```

Avoid creating unrelated `Model` instances when components must exchange entities; factories and processes receive a shared `Model` precisely so they refer to the same object graph.

## `ModelPart`: more than a mesh

A root ModelPart contains or provides access to:

| Entity/data | Role |
|---|---|
| Nodes | Coordinates, DOFs, historical data, non-historical data, flags |
| Elements | Domain physics and local equation contributions |
| Conditions | Boundary/interface/load contributions |
| Properties | Shared material, section, and constitutive-law data |
| Geometries | Connectivity and shape/integration operations without necessarily carrying physics |
| Master-slave constraints | Algebraic relations between DOFs |
| Tables | Piecewise data relationships, often time/value or field/property |
| SubModelParts | Hierarchical named groups/views of entities |
| `ProcessInfo` | Step-wide data such as dimension, time, and step number |
| Communicator | Local/distributed mesh and data-exchange abstraction |

This is why a ModelPart should not be thought of as only a list of coordinates and cells.

## Ownership and views

Root ModelParts own the actual entities. SubModelParts hold membership references to those same entities. In the example, node 1 is visible through:

```text
Domain
└── Boundary
    └── Inlet
```

There is still one node object with ID 1. Setting its data through `Inlet.GetNode(1)` changes what `Domain.GetNode(1)` sees.

This design makes overlapping semantic groups inexpensive. A node may simultaneously belong to a material domain, an inlet, a monitoring set, and an interface. It also means that removing entities requires care: root ownership and membership across all levels must remain consistent. Kratos supplies methods such as `RemoveNodesFromAllLevels` for explicit all-level removal.

## IDs, coordinates, and connectivity

Entity IDs are unique within their entity container in a root ModelPart. An element definition contains:

- a registered type name, for example `Element2D3N`;
- an element ID;
- node connectivity by ID;
- a reference to a `Properties` object.

The example creates a geometrical element:

```python
element = domain.CreateNewElement("Element2D3N", 1, [1, 2, 3], properties)
```

`Element2D3N` carries generic geometry but no application physics. Later, `TrussLinearElement3D2N` and `LaplacianElement2D3N` provide actual equations.

The geometry belongs to the entity and exposes operations such as `Area()`, `Length()`, integration points, shape functions, Jacobians, and local/global coordinate mapping.

## Elements versus conditions versus constraints

- An **element** normally integrates a domain weak-form contribution.
- A **condition** normally integrates a boundary/interface contribution or applies a concentrated load.
- A **fixed DOF** prescribes an unknown value and changes the algebraic problem.
- A **master-slave constraint** imposes an algebraic relation between DOFs.

These mechanisms are not interchangeable. A point-load condition contributes force to the residual; it does not fix displacement. A submodelpart named `Supports` is only a group until a process fixes its DOFs.

## Properties sharing

Many elements may reference the same Properties object. Changing that object changes the values subsequently read by every referencing entity. This is convenient for material domains, but an in-place edit is global to that property ID. Assign different property IDs when regions need independent values.

## Invariants worth checking

Before solving, check:

- expected entity counts in the root and important submodelparts;
- nonzero geometry measures and correct orientation;
- connectivity uses valid node IDs;
- every physics element has appropriate properties;
- boundary groups contain the entities expected by their processes;
- `DOMAIN_SIZE` agrees with the formulation.

## Work through these changes

1. Add a fourth node and a second triangle to form a unit square. Verify total area by summing element areas.
2. Create a `TopBoundary` SubModelPart that shares node 3 with `Inlet`. Set a non-historical value through one group and read it through the other.
3. Attempt to create a node using an existing ID but different coordinates. Read the error and explain the protected invariant.
4. Create two properties objects, assign one triangle to each, and store different `DENSITY` values.
5. Add a node to the nested `Inlet` submodelpart and inspect which ancestor ModelParts automatically contain it.

Next: [Chapter 02 — Variables, DOFs, and time](../02_variables_and_time/README.md).
