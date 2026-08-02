# Chapter 11 — Deep architecture, discovery, and extension strategy

At this point the examples have exercised each major Python layer. This chapter follows those calls into the registration system and the C++/Python boundary, then maps common changes to the correct extension point. The goal is to make an unfamiliar Application readable without relying on a copied case.

## Inspect the runtime registries

```bash
python3 tutorial/11_architecture_and_extension/inspect_runtime.py
```

## Three interacting layers

### 1. C++ framework and kernels

Performance-critical data structures and algorithms live in C++:

- entities and geometries;
- typed data containers;
- registered variables/components;
- element/condition/constitutive-law calculations;
- assembly, sparse algebra, strategies, and utilities;
- OpenMP/MPI infrastructure and serialization.

Python objects are bindings to these C++ objects, not pure-Python replicas.

### 2. Python orchestration

Python provides composable run logic:

- `AnalysisStage` and application stages;
- `PythonSolver` implementations and factories;
- Processes and OutputProcesses;
- configuration, experiment scripts, coupling logic, and tests.

This layer is easy to extend and inspect, while heavy node/element loops may be better placed in compiled utilities for performance.

### 3. Applications

An Application registers a coherent physics/tool set. Importing it executes registration so strings in MDPA/JSON can resolve to prototypes or Python modules. Applications may depend on other Applications; the required dependency set is determined by the build and source revision.

## Registration and factories

Kratos relies on names to instantiate configured components:

```text
"TrussLinearElement3D2N"
"KratosMultiphysics.StructuralMechanicsApplication.TrussConstitutiveLaw"
"assign_scalar_variable_process"
"skyline_lu_factorization"
```

At runtime these names resolve through legacy component registries, the hierarchical `Registry`, Python import factories, or specialized solver factories.

The inspect script demonstrates:

```python
KM.KratosGlobals.HasVariable("POINT_LOAD")
KM.KratosGlobals.GetVariableType("POINT_LOAD")
KM.Registry.HasItem("Processes.KratosMultiphysics.AssignScalarVariableProcess")
```

Import order matters: application-specific variables and prototypes appear only after the application is loaded.

## Shared ownership and object identity

Kratos entities are commonly managed through C++ shared pointers. Root and SubModelParts can refer to the same node/element/property. Consequences include:

- grouping is cheap;
- coupled ModelParts can share nodes or properties;
- mutations are visible through every reference;
- careless removal/mutation can affect multiple consumers;
- Python references may keep C++ objects alive.

Think in terms of an object graph, not file sections copied into isolated lists.

## Data flow through one solve

1. The solver allocates historical variables on the root ModelPart.
2. Input/modelers create nodes and physics entities using registered prototypes.
3. Materials populate Properties and constitutive laws.
4. The solver adds DOFs and prepares buffers/computing parts.
5. Processes write BC/load/source fields.
6. The strategy asks elements/conditions for local contributions through a scheme.
7. BuilderAndSolver maps local DOFs, assembles global algebra, and calls a LinearSolver.
8. The scheme/strategy updates nodal unknowns.
9. Elements/laws finalize state; processes inspect or output results.

For nonlinear/transient problems, parts of steps 5–8 repeat across steps and iterations.

## How to discover an unfamiliar component

Use a disciplined sequence:

1. **Identify its owner:** core or which Application?
2. **Import it and confirm registration.**
3. **Read defaults:** call the Python class's `GetDefaultParameters()` or intentionally validate a minimal block.
4. **Read specifications:** use `element.GetSpecifications()` when available.
5. **Inspect the matching Python factory/solver:** use the source from the same revision as the executable modules.
6. **Find official tests/examples:** tests often reveal minimal required variables/properties and expected values.
7. **Build a minimal verified case:** do not begin with a large model.

In a source checkout, start with `kratos/python_scripts/analysis_stage.py`, `kratos/python_scripts/process_factory.py`, and the selected Application's `python_scripts` directory. A packaged installation may flatten those modules under `KratosMultiphysics/`, but the interfaces are the same.

## Choosing the right extension point

| Need | Preferred extension |
|---|---|
| Change values at lifecycle hooks | Python Process |
| Coordinate run/order/stopping/monitoring | Application AnalysisStage subclass |
| Change scheme, strategy, computing part, or coupled solver logic | PythonSolver subclass/composition |
| Add fast mesh/data algorithm | C++ utility/process exposed to Python |
| Add domain/boundary weak-form contribution | C++ Element or Condition |
| Add material response | C++ ConstitutiveLaw |
| Add reusable component selection | Register component/prototype and expose settings |

Python prototypes may be appropriate for orchestration and experimentation, but production local physics belongs in compiled components for API integration, performance, thread safety, and serialization.

## Anatomy of a new element

A production element typically implements/checks:

- constructors, `Create`, and `Clone`;
- `EquationIdVector` and `GetDofList`;
- `CalculateLocalSystem`, LHS, and/or RHS;
- initialization/finalization hooks;
- mass/damping or explicit contributions when required;
- integration-point output;
- `Check` and `GetSpecifications`;
- serialization;
- application registration and Python exposure;
- unit, patch, convergence, and benchmark tests.

The local weak form, interpolation, quadrature, constitutive update, tangent consistency, and sign convention must be mathematically derived before implementation.

## Restart and serialization

A restart must restore more than nodal results. Depending on the formulation it may require:

- buffer and `ProcessInfo` history;
- element/condition internal state;
- constitutive-law history;
- constraints and properties;
- process/solver state;
- time and step counters.

Custom C++ components need serialization support. Stateful Python processes/stages must define how their state is saved/restored or reconstruct it deterministically. Validate restart by comparing an uninterrupted run with a split run.

## Parallel implications

For OpenMP:

- avoid Python loops in performance-critical per-entity calculations;
- do not mutate shared state unsafely from parallel C++ regions;
- know whether utilities are thread-safe.

For MPI:

- distinguish local, ghost, and interface entities;
- use communicator synchronization for fields;
- use `DataCommunicator` reductions for global monitors;
- ensure IDs/partitioning and output are distributed-aware.

## A debugging ladder

When a run fails, work upward:

1. environment/ABI and application import;
2. JSON types/defaults and file paths;
3. registration of variables/entities/laws/processes;
4. mesh counts, connectivity, geometry, orientation, submodelparts;
5. variables, DOFs, buffer, fixity, material completeness;
6. local element/condition `Check` and local system;
7. global DOF count, constraints, rank/null modes, scaling;
8. linear solver convergence;
9. nonlinear/time integration convergence;
10. physical verification, convergence studies, and validation.

Changing many solver parameters before checking levels 1–6 usually wastes time.

## Work through these investigations

1. Inspect the registered Processes after importing only core, then after importing an Application.
2. Print `GetDefaultParameters()` for the static structural solver and map five settings to solver-stack layers.
3. Inspect specifications for both linear and nonlinear truss elements and compare them.
4. Trace `StructuralMechanicsAnalysis.Run()` through the matching source tree and annotate every call that creates or modifies the ModelPart.
5. Design (without coding yet) a custom heat source: decide whether it belongs in a Process, Condition, or Element and justify the choice.
6. Write a restart equivalence test plan for a history-dependent constitutive law.

Next: [Chapter 12 — Capstone](../12_capstone/README.md).
