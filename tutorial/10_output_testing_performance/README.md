# Chapter 10 — Output, testing, diagnostics, and performance

A converged solver has only shown that its configured algebraic problem met a stopping criterion. It has not shown that the input represents the intended problem, that discretization error is small, or that the physical model is valid. Output, automated checks, balance tests, convergence studies, and reproducible runtime records are part of the analysis.

## Run the examples and tests

```bash
python3 tutorial/10_output_testing_performance/run_heat_with_vtk_output.py
python3 -m unittest tutorial/10_output_testing_performance/test_tutorial_cases.py -v
python3 tutorial/10_output_testing_performance/runtime_controls.py
```

## Output is a process with scheduling

`run_heat_with_vtk_output.py` loads the Chapter 09 Parameters and programmatically attaches a VTK OutputProcess. The stage then invokes the output lifecycle at the correct point.

Important settings include:

- target `model_part_name`;
- ASCII or binary file format;
- output precision;
- step- or time-based control and interval;
- output directory;
- historical nodal, non-historical nodal, elemental, conditional, and integration-point variables.

The example writes ASCII VTK under:

```text
tutorial/10_output_testing_performance/generated/vtk/
```

Open the result in ParaView or another VTK reader. ASCII is convenient for learning/debugging; binary is normally smaller and faster for large results.

The VTK process clears its configured output directory at the start of a non-restart run when folder output is enabled. Therefore configure a dedicated generated-results directory, never a directory containing source input or unrelated user data.

## Choose output intentionally

Writing every field at every step can dominate runtime and storage. Output should answer a question:

- fields needed for visualization;
- reactions or balances needed for verification;
- point/history data needed for plots;
- integration-point stress/flux needed for engineering interpretation;
- diagnostics needed only during development.

For a large model, prefer sparse monitoring output during iterations and less frequent field snapshots. Ensure a derived field is computed before requesting it.

## Verification, validation, convergence, conservation

These terms answer different questions:

- **Code/case verification:** are equations/configuration solved correctly? Compare against analytical/manufactured solutions and benchmark tests.
- **Solution verification:** is discretization/iteration/time-step error acceptably small? Perform mesh, time-step, and tolerance studies.
- **Validation:** does the mathematical model represent measured physical reality for the intended use?
- **Conservation/equilibrium:** do global/local balances close within an explained tolerance?

The truss and heat tests are verification cases. They do not validate Kratos for an arbitrary real structure or thermal system.

## Integration tests

`test_tutorial_cases.py` runs the complete structural and heat entry points as subprocesses with the same interpreter. Testing the public entry points catches:

- import/environment problems;
- file-path and factory construction problems;
- solver failures;
- violated numerical assertions.

Run all tutorial checks with:

```bash
python3 run_all.py
```

A production test hierarchy should include:

1. unit tests for custom calculations/processes;
2. tiny component tests for local systems and settings validation;
3. integration tests for complete input-to-result workflows;
4. benchmark/regression tests with tolerances appropriate to platform and algorithm;
5. independent validation datasets where physical prediction matters.

Avoid regression tests that merely freeze an unexplained number. Record why the reference is correct, its units, and the acceptable tolerance.

## Logging and checks

Use echo levels and `KM.Logger` to expose the layer currently under investigation. Before solving, check:

- imported component names and versions;
- mesh and submodelpart counts;
- material/property assignments;
- required variables and DOFs;
- fixed/free DOF counts and connected components;
- characteristic scales and units;
- solver/strategy settings after defaults;
- time/buffer initialization.

After solving, check:

- convergence reason and iteration counts;
- residual/increment norms;
- global reactions versus loads/sources;
- min/max and non-finite values;
- expected symmetry/invariants;
- mesh/time/tolerance sensitivity;
- restart equivalence when restarts are used.

## Threads and timing

When Kratos is built with OpenMP, `runtime_controls.py` demonstrates the process-wide thread controls:

```python
KM.ParallelUtilities.GetNumThreads()
KM.ParallelUtilities.SetNumThreads(n)
```

Thread count is process-global. Set it before computational work, document it, and restore it in reusable library code. More threads can be slower for small problems due to overhead and memory bandwidth. Measure representative workloads rather than assuming maximum core count is optimal.

The node-creation timing example is a deterministic mechanics-free operation; it teaches the API but is not a solver benchmark. Meaningful performance studies need:

- a representative model and solver;
- warm-up and repeated runs;
- fixed input and convergence criteria;
- wall time separated by stage when possible (I/O, assembly, linear solve, output);
- memory usage and linear/nonlinear iteration counts;
- thread/process affinity and hardware details.

## OpenMP versus MPI

- **OpenMP:** threads share one process memory space; Kratos containers remain local to the process.
- **MPI:** the ModelPart is partitioned across processes with local/ghost/interface entities; collectives use a `DataCommunicator`.

Custom global sums must use communicator reductions in distributed runs. A Python `sum` over local nodes is not a global sum under MPI. Parallel correctness comes before parallel speed.

## Numerical performance before hardware performance

The greatest speedups often come from:

- choosing a formulation appropriate to the problem;
- improving mesh quality;
- using realistic convergence tolerances;
- selecting a suitable sparse solver/preconditioner;
- avoiding needless matrix reformation when mathematically valid;
- reducing output volume;
- scaling variables and units to avoid conditioning problems.

Never loosen convergence or alter physics merely to make a timing number smaller without quantifying error.

## Work through these changes

1. Open the generated VTK file and locate `TEMPERATURE` in the point data.
2. Change `output_interval` so a four-step case writes only every second step.
3. Add a failing heat-boundary value and confirm the integration test reports useful captured output.
4. Write a test for the process ramp values at times before, inside, and after its interval.
5. Time the structural sweep with 1, 2, and 4 threads. Explain why the tiny case should not scale.
6. Add a global balance check to the heat case using `REACTION_FLUX` on both fixed boundaries.

Next: [Chapter 11 — Architecture and extension](../11_architecture_and_extension/README.md).
