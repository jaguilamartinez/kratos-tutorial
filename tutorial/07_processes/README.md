# Chapter 07 — Processes and lifecycle-driven customization

A Process is a small unit of behavior called at defined points in an analysis. Boundary conditions, loads, initialization, checks, monitoring, and output are all natural process responsibilities. Keeping these actions outside the solver makes them reusable and configurable.

## Run the example

```bash
python3 tutorial/07_processes/run_with_process.py
```

Expected monitor output rises linearly from 250 N to 1000 N over four steps, with displacement proportional to load.

## The process contract

A process derives from `KM.Process` and may implement these hooks:

| Hook | Typical use |
|---|---|
| `ExecuteInitialize` | One-time setup after model import and process construction |
| `ExecuteBeforeSolutionLoop` | Initialization requiring an initialized solver |
| `ExecuteInitializeSolutionStep` | Time-dependent BCs/loads or per-step preparation before solving |
| `ExecuteFinalizeSolutionStep` | Monitoring or state updates after solving |
| `ExecuteBeforeOutputStep` | Derive data only when output will be written |
| `ExecuteAfterOutputStep` | Clean up temporary output data |
| `ExecuteFinalize` | Close files and release one-run resources |
| `Check` | Validate model parts, variables, settings, and compatibility |

Implement only the hooks your behavior needs.

## Factory construction

The module-based process factory used by this example imports the module named in JSON and calls:

```python
def Factory(settings, model):
    return RampLoadProcess(model, settings["Parameters"])
```

Core/Application processes add `kratos_module`; user modules omit it and must be importable on `sys.path`. Since `run_with_process.py` resides beside `ramp_load_process.py`, launching the entry point places that directory on `sys.path`. Mesh and material paths are resolved separately as absolute paths.

Kratos also supports registry-based process construction using a `name` path. The module factory remains part of many existing cases and is useful for project-local Python processes that are not registered in an Application.

## The ramp process

`ramp_load_process.py`:

1. validates settings and assigns defaults;
2. rejects an empty or reversed time interval;
3. resolves `Structure.LoadPoint` once in the constructor;
4. checks that the group has nodes and `POINT_LOAD` has been allocated;
5. reads current `TIME` from the group's shared `ProcessInfo`;
6. interpolates load across the configured interval;
7. writes historical `POINT_LOAD` before the solve;
8. reads displacement and prints monitoring data after the solve.

It writes an `Array3` to the registered application variable. The point condition reads this value while calculating its contribution.

## Lifecycle ordering matters

For each step, the default stage performs process initialization before solver initialization/prediction/solve, then process finalization after solver finalization. Therefore:

- a load needed by the current solve belongs in `ExecuteInitializeSolutionStep`;
- a reaction/displacement produced by the solve belongs in `ExecuteFinalizeSolutionStep`;
- output-only derived fields may belong in `ExecuteBeforeOutputStep`.

Putting a load update in `ExecuteFinalizeSolutionStep` introduces a one-step lag.

## Process versus AnalysisStage versus solver

Use a **Process** when behavior is modular and hook-based:

- apply or release a BC;
- update a source/load;
- initialize or transform values;
- monitor/check results;
- write custom output.

Use an **AnalysisStage subclass** when changing orchestration or coordinating several behaviors:

- custom stopping criteria;
- stage-level data collection;
- changing geometry/material at documented stage hooks;
- special sequencing around existing processes/solver.

Use a **PythonSolver subclass** when changing physics setup or solution algorithms:

- scheme, builder, convergence criterion, strategy;
- computing ModelPart construction;
- coupled physics logic.

Use a new **C++ element/condition/law** when the local physics itself changes.

## Process design practices

- Validate settings in the constructor and fail early.
- Resolve ModelParts/variables once rather than by string inside every node loop.
- Keep hidden mutable state minimal and document restart behavior.
- Use `ProcessInfo[TIME]`, not a private unsynchronized clock.
- Use communicator-aware reductions for global quantities in MPI.
- Make `Check()` meaningful for production processes.
- Ensure finalization closes files even when no output step occurs.

## Work through these changes

1. Change the ramp to a triangular load that returns to zero at time 4.
2. Accept a load direction vector and validate that it has nonzero norm.
3. Extend `Check` to verify that every target node belongs to at least one point-load condition.
4. Store history in the process and expose it through a method; retrieve the process from a custom stage.
5. Replace the custom ramp with the built-in expression support of an assignment process and compare maintainability.
6. Add an interval `[1, 3]` outside which the process applies zero, then predict all four step results.

Next: [Chapter 08 — Custom AnalysisStage](../08_custom_analysis_stage/README.md).
