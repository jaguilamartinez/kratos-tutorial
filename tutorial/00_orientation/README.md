# Chapter 00 — Runtime, Core, and Applications

Before looking at a model, establish which Kratos runtime is executing it. Kratos includes compiled Python modules, so the Python interpreter, Kratos build, enabled Applications, machine architecture, and parallel mode all belong to the definition of a run.

## Run the runtime report

```bash
python3 tutorial/00_orientation/check_installation.py
```

The program imports Core, StructuralMechanicsApplication, and ConvectionDiffusionApplication, then reports their module locations and runtime information. If it succeeds, the remaining examples have the Applications they need.

Record the following for any result that must be reproduced:

- Kratos version or source revision;
- Python version and executable;
- operating system and processor architecture;
- build type and relevant compiler options;
- enabled Applications;
- OpenMP thread count or MPI process count;
- mesh, material, parameter, and custom Python files.

Numerical behavior can change when any of these change. Keeping this information with the result makes it possible to distinguish an environment problem from a modeling or solver problem.

## Core and Applications

The Core module provides facilities shared by many fields:

- `Model`, `ModelPart`, nodes, geometries, properties, elements, conditions, and constraints;
- typed variable and data containers;
- matrices, vectors, linear solvers, schemes, strategies, and assembly tools;
- process, input/output, serialization, logging, and parallel interfaces;
- component registries and factories.

An Application extends that base with a coherent set of physics or algorithms. Importing StructuralMechanicsApplication registers structural elements, conditions, variables, constitutive laws, solvers, and processes. ConvectionDiffusionApplication does the same for scalar transport and thermal problems.

```python
import KratosMultiphysics as KM
import KratosMultiphysics.StructuralMechanicsApplication as SMA
```

Registration is why an MDPA file can name an element with a string such as `TrussLinearElement3D2N`. The reader looks up that name and creates the registered prototype. If the owning Application has not been imported—or was not compiled—the lookup fails.

Application imports can have dependencies. A structural build may load a constitutive-law Application as part of its initialization. Treat those startup messages as useful evidence of the components present in the process.

## Python and compiled-module compatibility

Pure Python packages can often move between Python patch releases and platforms. Kratos distributions commonly include native modules, which must match the interpreter ABI and processor architecture for which they were built.

Typical symptoms of a mismatch are:

| Symptom | Check |
|---|---|
| `ModuleNotFoundError` | `sys.executable`, environment activation, `PYTHONPATH`, installation path |
| Native module load error | Python minor version, processor architecture, dependent shared libraries |
| Unknown element, condition, law, or variable | owning Application import and build configuration |
| Case changes after an upgrade | source revision, component defaults, parameter schema, solver settings |

Use the same interpreter to install/build Kratos, run examples, and run tests. In automated jobs, invoke that interpreter explicitly instead of relying on whichever `python3` appears first on `PATH`.

## Parallel mode

`KM.IsDistributedRun()` distinguishes an MPI run from a local/OpenMP run. `KM.ParallelUtilities.GetNumThreads()` reports the configured thread count. These modes affect custom code:

- an OpenMP run shares one process memory space;
- an MPI run partitions the model and requires communicator operations for global values;
- a sum over `model_part.Nodes` is only a local sum in a distributed run;
- reproducible performance records must include thread/process count.

Chapter 10 returns to parallel execution and timing. Chapter 11 explains the communicator and extension implications.

## Work through these checks

1. Run the report with the interpreter normally used for Kratos and save the output.
2. Run `python3 -c "import sys; print(sys.executable)"` and confirm that it matches your expectation.
3. Comment out one Application import, then inspect which application-specific variable names are no longer available in a fresh process.
4. Print `KM.KratosGlobals.GetVariableType("DISPLACEMENT")` after importing StructuralMechanicsApplication.
5. In a separate environment or build, compare the runtime report before attempting to compare numerical results.

Continue with [Chapter 01 — Model and ModelParts](../01_model_and_modelparts/README.md).
