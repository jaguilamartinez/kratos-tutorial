# Chapter 12 — Capstone: from one case to a computational study

The final chapter turns one verified case into a numerical study. The included program varies one input, creates a clean analysis for each point, extracts a response, and checks an invariant. The same pattern scales to convergence studies, material sweeps, uncertainty analysis, and design loops.

## Run the sweep

```bash
python3 tutorial/12_capstone/parameter_sweep.py
```

## The included sweep

The script solves the Chapter 06 truss for four loads. Each iteration:

1. rereads pristine `ProjectParameters.json`;
2. changes only the x load value;
3. creates a fresh Model and AnalysisStage;
4. runs the complete simulation;
5. extracts tip displacement;
6. computes effective stiffness `F/u`;
7. asserts `F/u = EA/L`.

The result is CSV-like:

```text
force_N,displacement_m,effective_stiffness_N_per_m
250.0,...,2.100000e+09
...
```

Fresh Models and Parameters prevent one run's buffers, process mutations, properties, or solver state from contaminating another.

## Turn it into an auditable experiment

For a real study, create a record per case containing:

- case ID and timestamp;
- Kratos/Python version and source artifact;
- input parameter values and units;
- mesh/material identifiers or hashes;
- thread/process count;
- convergence settings and achieved iteration counts;
- requested response quantities;
- verification/balance/error metrics;
- run status and diagnostic message;
- elapsed time and output location.

Write data atomically and never infer success merely because an output file exists.

## Core capstone assignment: a triangular truss

Build a stable 2D triangular truss using 3D truss elements with z constrained:

```text
            node 3
             /\
            /  \
           /    \
       node 1──node 2
```

Requirements:

1. Define nodes, three elements, supports, and load-point condition in MDPA.
2. Use at least two Properties IDs or explain why one is sufficient.
3. Apply constraints/loads through Processes.
4. Derive a reference solution using equilibrium/stiffness or an independent calculation.
5. Check global force balance and at least one symmetry relation.
6. Perform a load sweep and confirm linearity.
7. Write VTK displacement and reaction output.
8. Add an integration test with documented tolerances.
9. Introduce one deliberate modeling error and document its diagnostic signature.

## Advanced tracks

### A. Geometric nonlinearity

Move from `TrussLinearElement3D2N` to a nonlinear truss formulation. Use incremental loading and a nonlinear strategy. Study:

- load-step sensitivity;
- residual/displacement convergence;
- tangent consistency;
- deformed geometry;
- linear versus nonlinear response;
- snap-through/path-following limitations for a shallow two-bar truss.

If a standard load-controlled Newton method cannot trace a limit point, explain why an arc-length/path-following strategy is required rather than hiding nonconvergence.

### B. Transient heat diffusion

Extend Chapter 09 with heat capacity and an initially cold domain. Study:

- time integration and buffer requirements;
- spatial and temporal convergence separately;
- energy balance;
- approach to the stationary solution;
- restart equivalence halfway through the simulation.

### C. Coupled thermo-mechanics

Use a shared or mapped mesh for temperature and displacement. Define:

- coupling direction (one-way or two-way);
- variable transfer and timing;
- thermal expansion material data;
- convergence of staggered iterations if two-way;
- independent limiting cases (zero thermal expansion, uniform temperature, mechanically free body).

### D. Custom component development

Create a small Application component only after deriving and testing its mathematics. Start with:

- a custom Process in Python;
- then a compiled utility or element if local/per-entity performance or weak-form physics requires it;
- registration, specifications, serialization, and focused tests;
- a patch test and mesh-convergence study.

## Scientific checks for every track

At minimum address:

- **dimensions:** every equation/input uses a consistent unit system;
- **boundary completeness:** eliminate only intended null modes;
- **equilibrium/conservation:** reactions balance applied loads or sources;
- **convergence:** iterative residuals and increments satisfy justified tolerances;
- **discretization:** mesh/time-step refinement trends are quantified;
- **limiting cases:** zero loads, symmetric data, very stiff/soft limits behave as expected;
- **independence:** compare with an analytical, manufactured, experimental, or separately implemented reference;
- **reproducibility:** a clean process can rerun the case from archived inputs.

## Completion checklist

A complete case description should answer each of these questions without relying on a preprocessor or GUI:

1. which registered entity supplies each weak-form contribution;
2. where every required variable is stored and why it is historical or not;
3. how each DOF enters the global system and how constraints remove null modes;
4. how Properties and constitutive laws affect the local tangent/residual;
5. which scheme, builder, strategy, criterion, and linear solver are active;
6. the exact order in which processes and solver hooks execute;
7. what evidence supports the numerical result and which error sources remain;
8. where to extend the system for a new load, workflow, solver, or physical law.

Return to the [course README](../../README.md), select an advanced track, and preserve the small verified examples as regression tests while you expand complexity.
