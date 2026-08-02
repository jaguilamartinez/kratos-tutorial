# Chapter 09 — Reusing the framework for heat diffusion

The structural examples used displacement DOFs and truss elements. This chapter uses the same ModelPart, Parameters, process, solver, and AnalysisStage concepts to solve a scalar diffusion equation. The comparison shows which parts of Kratos are general and which belong to a physics Application.

## Run the example

```bash
python3 tutorial/09_heat_diffusion/run_heat_problem.py
```

## Governing problem

For constant conductivity `k` and no volumetric source, steady heat conduction is:

```text
-∇·(k ∇T) = 0  in Ω
T = 0            on x=0
T = 100          on x=1
q_n = 0          on y=0 and y=1
```

On the unit square, the exact solution is:

```text
T(x,y) = 100x
```

The mesh has four linear triangles meeting at `(0.5,0.5)`. A linear finite element reproduces a linear field exactly (up to roundoff), so the centre node must be 50.

## Weak-form interpretation

Multiplying by a test function and integrating by parts produces a domain gradient term and a boundary flux term. The Laplacian element contributes the domain conductivity matrix. Prescribed temperatures are essential (Dirichlet) constraints on temperature DOFs. The omitted top/bottom flux corresponds to the natural zero-flux condition.

A nonzero flux would require the appropriate boundary condition entity/process so it contributes to the RHS.

## Convection-diffusion variable mapping

The same solver family supports several scalar transport choices by mapping roles to registered variables:

| Role | This case |
|---|---|
| Unknown | `TEMPERATURE` |
| Diffusion coefficient | `CONDUCTIVITY` |
| Volume source | `HEAT_FLUX` |
| Surface source | `FACE_HEAT_FLUX` |
| Reaction | `REACTION_FLUX` |
| Density/specific heat | `DENSITY`, `SPECIFIC_HEAT` (important in transient cases) |
| Convection velocity | `CONVECTION_VELOCITY` |

The solver stores a `ConvectionDiffusionSettings` object in `ProcessInfo`, and elements query these semantic roles rather than hard-coding only one scalar field.

## Element replacement

The MDPA contains generic `Element2D3N` connectivity. During `PrepareModelPart`, the solver uses:

```json
"element_replace_settings": {
    "element_name": "LaplacianElement",
    "condition_name": "ThermalFace"
}
```

With domain size 2 and three-node connectivity, this resolves to `LaplacianElement2D3N`. Replacement separates mesh topology from the chosen physics. It is useful for solving different fields on the same connectivity, but only when geometry and required variables/properties are compatible.

## Materials and nodal coefficients

`Materials.json` assigns conductivity, density, specific heat, and zero source to property ID 1. The convection-diffusion solver also transfers configured material variables to nodes because these formulations access coefficients nodally.

The log line saying no constitutive law is defined is informational here: the Laplacian element reads scalar transport coefficients and does not need a structural constitutive law.

## Boundary processes

Two built-in scalar assignment processes fix temperature on:

- `ThermalDomain.ColdBoundary` at 0;
- `ThermalDomain.HotBoundary` at 100.

The top and bottom need no condition for zero natural flux. This is a weak-form property, not a missing model input.

## Why this chapter matters architecturally

Compare Chapters 06 and 09. Both use:

- `Model` and ModelParts;
- MDPA and materials;
- Parameters and factories;
- processes for essential conditions;
- a PythonSolver and AnalysisStage lifecycle;
- a sparse direct linear solver;
- programmatic verification.

The application changes the variables, elements, materials interpretation, and solver construction—not the whole framework.

## Extending to transient diffusion

For transient heat conduction:

```text
ρ c ∂T/∂t - ∇·(k∇T) = Q
```

you need a transient solver, appropriate element/time integration, buffer history, density/specific heat, time step and total time, and initial temperature. Then verify temporal convergence as well as spatial convergence. A stable result is not automatically an accurate result.

## Work through these changes

1. Change the hot boundary to 200 and predict every nodal temperature.
2. Change conductivity from 10 to 100. Explain why the temperature field stays the same but boundary reaction flux changes.
3. Add a second centre-line node arrangement and check that the linear field remains exact.
4. Apply a nonzero source. Derive or obtain a reference solution and quantify error.
5. Add VTK output for `TEMPERATURE` and `REACTION_FLUX` (Chapter 10 already provides one implementation).
6. Convert to a transient solver, initialize `T=0`, and study time-step refinement toward the stationary solution.

Next: [Chapter 10 — Output, testing, and performance](../10_output_testing_performance/README.md).
