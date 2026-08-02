# Glossary

**AnalysisStage**  
Top-level lifecycle controller. It coordinates model import, solver initialization, processes, time advancement, solution steps, output, and finalization. Application-specific stages derive from the core `AnalysisStage`.

**Application**  
A plug-in-like Kratos module that registers physics-specific variables, elements, conditions, constitutive laws, solvers, processes, and utilities. Importing an application makes its components available.

**BuilderAndSolver**  
The component that numbers equations, gathers element/condition contributions, assembles the global matrix and vector, incorporates constraints, and calls the linear solver. The scheme/strategy uses the resulting increment to update DOFs.

**Condition**  
A boundary or lower-dimensional entity that contributes to the discrete equations, such as a point force, traction, flux, or interface term. A condition is not the same thing as a prescribed DOF.

**Constitutive law**  
The material response model used by an element, commonly mapping strain measures to stresses and tangent moduli.

**Convergence criterion**  
The test used by a nonlinear strategy to stop iterating, commonly based on residual or solution-increment norms with relative and absolute tolerances.

**Computing ModelPart**  
The ModelPart or SubModelPart whose elements, conditions, constraints, and DOFs are passed to the solution strategy. It may be the root ModelPart or a solver-prepared subset.

**DataCommunicator**  
Kratos abstraction for collective communication. In serial/OpenMP it is local; in distributed builds it wraps MPI communication.

**DOF (degree of freedom)**  
An unknown attached to a node, such as `DISPLACEMENT_X` or `TEMPERATURE`. A stored variable is not automatically a DOF. DOFs can be free or fixed and may have associated reaction variables.

**Element**  
An entity that implements a domain contribution to the discretized physics. It calculates a local tangent/stiffness matrix and residual/right-hand side and declares the associated DOFs.

**Essential (Dirichlet) boundary condition**  
A prescribed value of an unknown, normally represented by fixing a DOF and setting its value.

**Flag**  
A compact boolean state such as `ACTIVE`, `BOUNDARY`, or `TO_ERASE`, independent of the typed variable database.

**FlowGraph**  
A separate browser-based node editor that generates Kratos configuration from connected workflow components. Its editable graph and the generated ProjectParameters are different artifacts.

**Historical data**  
Nodal solution-step data stored in a circular buffer. Access it with `GetSolutionStepValue`/`SetSolutionStepValue`.

**Linear solver**  
The component that solves the assembled algebraic system. Direct and iterative solvers have different memory, scaling, symmetry, definiteness, and preconditioning requirements.

**Master-slave constraint**  
An algebraic relation that expresses one or more slave DOFs in terms of master DOFs. It is used for periodicity, multi-point constraints, tying, and related kinematic relations.

**MDPA**  
Kratos ModelPart text format. It serializes nodes, properties, elements, conditions, initial nodal/entity data, tables, and submodelpart membership.

**Model**  
The top-level container and name-based index of root ModelParts in one simulation.

**ModelPart**  
The central simulation data structure containing mesh entities, properties, submodelparts, `ProcessInfo`, tables, communicator data, and registered historical-variable layout.

**Modeler**  
A lifecycle component that imports, creates, transforms, or prepares geometry and ModelParts before solver setup.

**Natural (Neumann) boundary condition**  
A flux, traction, or related term that enters through the boundary part of a weak form. A zero natural condition is often implicit when no boundary contribution is added.

**Newton-Raphson method**  
A nonlinear iteration that repeatedly assembles a residual and tangent system, solves for an increment, and updates the trial solution until a convergence criterion is met.

**Non-historical data**  
Typed data attached directly to a node, element, condition, or properties object without a time buffer. Access it with `GetValue`/`SetValue` or bracket syntax where supported.

**OutputProcess**  
A process with output scheduling (`IsOutputStep`) and writing (`PrintOutput`) in addition to lifecycle hooks.

**Orchestrator**  
The driver of a multistage Kratos Project. It selects stage order and coordinates stage preprocessing, execution, postprocessing, output data, and checkpoints.

**Parameters**  
Kratos's typed, mutable wrapper around JSON data, used for configuration and runtime factories.

**Process**  
A lifecycle-aware unit of behavior used for constraints, loads, initialization, checks, model modification, monitoring, or output.

**ProcessInfo**  
ModelPart-wide typed data such as `TIME`, `DELTA_TIME`, `STEP`, and `DOMAIN_SIZE`, passed to elements and conditions during calculations.

**Project**  
The multistage container that owns a shared Model, project settings, stage output data, active stages, and checkpoint state. It is distinct from the conventional use of “project” for a case directory.

**ProjectParameters**  
The conventional JSON configuration passed to a Kratos AnalysisStage or multistage Project. It has no single universal schema: the selected stage, solver, factories, processes, modelers, and outputs own different subtrees.

**Properties**  
A shared typed-data container referenced by elements/conditions, normally holding material and section values and a constitutive law.

**Registry**  
The hierarchical catalog of component names, prototypes, and Python module information used by factories.

**Reaction**  
The force, flux, or other equation imbalance associated with a prescribed DOF. Reactions are commonly used to check global equilibrium or conservation.

**Residual**  
The imbalance that remains after evaluating the current trial solution. Sign conventions differ between components; reason from the equation implemented by the element/condition and strategy.

**Scheme**  
Defines update rules and, for transient problems, how time derivatives and effective contributions are computed.

**Strategy**  
Controls the solve algorithm: initialization, prediction, assembly, linear solve, nonlinear iterations, convergence checks, and finalization.

**SubModelPart**  
A hierarchical view/group of root-owned entities. It usually represents a material domain, boundary, load set, or computing domain; it does not duplicate the entities.

**Variable**  
A globally registered, strongly typed key such as `TEMPERATURE`, `DISPLACEMENT`, or `YOUNG_MODULUS`.

**Weak form**  
The integral form of a governing equation used to derive finite-element contributions. Integration by parts typically moves derivatives from the unknown to test functions and exposes natural boundary terms.
