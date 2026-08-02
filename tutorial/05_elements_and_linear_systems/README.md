# Chapter 05 — From element equations to the global solve

The next step is to connect ModelPart entities to the algebra Kratos solves. One example asks a real structural element for its local tangent and residual. The other assembles two scalar springs by hand and sends the reduced sparse system to a Kratos linear solver.

## Run the examples

```bash
python3 tutorial/05_elements_and_linear_systems/inspect_truss_element.py
python3 tutorial/05_elements_and_linear_systems/assemble_and_solve.py
```

## The discrete nonlinear problem

Many Kratos implicit problems can be written conceptually as:

```text
R(u) = f_external - f_internal(u) = 0
```

At nonlinear iteration `k`, a tangent problem is solved:

```text
K_t(u_k) Δu = R(u_k)
u_(k+1) = u_k + Δu
```

For a linear static problem, the tangent is constant and one solve is sufficient. Sign conventions for the returned local RHS/residual depend on the component and strategy, so use the formulation's implementation and tests rather than assuming every `CalculateRightHandSide` returns a raw external load.

## What an element contributes

An element receives its geometry, Properties, nodal values, and `ProcessInfo`. Its key responsibilities include:

- calculating local left-hand-side/tangent contributions;
- calculating local right-hand-side/residual contributions;
- declaring its DOFs and equation IDs;
- checking required variables, properties, and geometry;
- optionally calculating mass, damping, integration-point output, explicit contributions, and sensitivities.

`inspect_truss_element.py` creates a one-metre axial bar with:

```text
E = 210 GPa
A = 0.01 m²
L = 1 m
EA/L = 2.1×10⁹ N/m
```

The 3D two-node element has local DOF order:

```text
[ux1, uy1, uz1, ux2, uy2, uz2]
```

Because the bar is aligned with global x, only the x rows/columns are nonzero. Its axial block is:

```text
(EA/L) [[ 1, -1],
        [-1,  1]]
```

Rotating the bar would distribute axial stiffness among global components through its transformation.

## `GetSpecifications()` is executable documentation

Registered elements can publish JSON specifications. The truss reports required DOFs, variables, compatible geometry and constitutive-law characteristics, supported time integration, and matrix properties.

Use specifications to answer questions such as:

- Does this element require rotations or only translations?
- Is it compatible with implicit dynamics?
- Which nodal fields may be output?
- Which constitutive law dimension/strain size is expected?

Specifications help diagnose compatibility and missing data. They do not replace formulation documentation or validation benchmarks.

## Global assembly

The builder maps local DOFs to equation IDs and accumulates:

```text
K[I(a), I(b)] += K_e[a, b]
b[I(a)]       += r_e[a]
```

where `I(a)` maps a local DOF to a global equation index. Contributions from every element and condition sharing a DOF accumulate into the same row/column.

`assemble_and_solve.py` demonstrates two scalar springs:

```text
fixed node 0 ── k=1000 ── node 1 ── k=1000 ── node 2 → 100 N
```

After assembly:

```text
K = [[ 1000, -1000,     0],
     [-1000,  2000, -1000],
     [    0, -1000,  1000]]
```

The first displacement is prescribed to zero. Eliminating its equation gives a nonsingular free system with `u1=0.1 m`, `u2=0.2 m`.

## The implicit solver stack

| Layer | Main responsibility |
|---|---|
| Element/Condition | Local physics and contributions |
| Scheme | Unknown update and time-integration/effective contributions |
| BuilderAndSolver | DOF set, equation numbering, assembly, constraints, solve dispatch |
| LinearSolver | Solve `Ax=b` for assembled algebraic system |
| ConvergenceCriterion | Decide whether nonlinear iteration has converged |
| Strategy | Coordinate prediction, assembly, solve, update, and nonlinear loop |
| PythonSolver | Select/configure the above for one physics Application |
| AnalysisStage | Coordinate time loop, processes, solver, and output |

When changing a parameter, identify which layer owns it. A Krylov tolerance belongs to the linear solver; a Newton residual tolerance belongs to the nonlinear convergence criterion; a time scheme parameter belongs to the scheme or solver.

## Constraints and singularity

The unconstrained spring matrix has a rigid translation mode. Likewise, structural models without sufficient supports produce singular systems. Singularities can also arise from:

- disconnected nodes or components;
- DOFs that no element/condition couples;
- zero/invalid material or geometric properties;
- incompatible element orientation or degeneracy;
- redundant/inconsistent constraints;
- a physical null space that requires a reference value (for example pressure).

Do not “fix” a singular model by adding arbitrary constraints until you understand the missing physical condition.

## Linear solvers

The manual example uses `skyline_lu_factorization`, a direct solver suited to tiny deterministic examples. Large sparse systems often use iterative solvers and preconditioners, where scaling, tolerance, maximum iterations, symmetry, definiteness, and matrix conditioning matter. Solver choice must follow the matrix properties of the formulation and problem size.

## Work through these changes

1. Change the second spring stiffness to 2000 N/m and derive both displacements before running.
2. Apply the force at node 1 instead of node 2 and explain the unloaded spring response.
3. Rotate the truss element 45 degrees in the xy plane and inspect its local matrix in global coordinates.
4. Set a trial displacement on node 2, recalculate the local RHS, and investigate its residual sign convention.
5. Replace the direct solver with an available iterative solver and compare residual/error on this tiny system.
6. Explain which layer you would modify to add: a constitutive model, a nonlinear convergence test, an MPC, or output every ten steps.

Next: [Chapter 06 — Complete structural analysis](../06_complete_structural_analysis/README.md).
