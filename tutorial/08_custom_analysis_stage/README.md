# Chapter 08 — Customizing the AnalysisStage safely

Use a custom AnalysisStage when the change concerns the order or coordination of a run rather than a reusable action or a new physical formulation. Deriving from the Application's stage preserves its solver construction, process handling, and future fixes while exposing narrow lifecycle hooks.

## Run the example

```bash
python3 tutorial/08_custom_analysis_stage/monitoring_analysis.py
```

The custom stage doubles the truss area after material import, reducing displacement by half, and records time, tip displacement, and reaction after the step.
It rejects non-positive area scale factors before constructing the solver.

## Derive from the application's stage

The class derives from `StructuralMechanicsAnalysis`, not directly from the core `AnalysisStage`:

```python
class MonitoringStructuralAnalysis(StructuralMechanicsAnalysis):
    ...
```

This retains StructuralMechanicsApplication's solver factory, compatibility handling, process setup, and output behavior.

Do not copy the entire `Run()` method or time loop to add one action. That freezes internal behavior at the copied revision. Override the narrowest documented hook.

## Hooks used in the example

### `ModifyInitialProperties`

The base lifecycle invokes this after model/material import and DOF addition, before solver initialization. The Properties object is therefore available and can be modified before the element/strategy initializes:

```python
properties = self.model["Structure"].GetProperties()[1]
properties[SMA.CROSS_AREA] *= self.area_scale
```

Because Properties are shared, all elements referencing ID 1 see the new area.

### `FinalizeSolutionStep`

The override first preserves application behavior:

```python
super().FinalizeSolutionStep()
```

It then reads the converged step's values. Omitting the base call would skip solver and process finalization.

### `GetFinalData`

Returning a plain dictionary gives external experiment drivers a stable interface without reaching into private solver fields.

## Lifecycle extension points

| Method | Suitable use |
|---|---|
| `ModifyInitialProperties` | Edit imported material/property data before solver initialization |
| `ModifyInitialGeometry` | Adjust imported geometry before solver initialization |
| `ModifyAfterSolverInitialize` | Actions that require fully initialized strategy/solver |
| `ApplyBoundaryConditions` | Usually leave process invocation intact; augment only with care |
| `ChangeMaterialProperties` | Step-dependent material changes |
| `InitializeSolutionStep` | Stage-level work before prediction/solve; call base implementation |
| `FinalizeSolutionStep` | Stage-level work after solve; call base implementation |
| `OutputSolutionStep` | Custom scheduling/coordination around output |
| `KeepAdvancingSolutionLoop` | Alternative stopping condition |
| `GetFinalData` | Stable programmatic result summary |

Read `kratos/python_scripts/analysis_stage.py` from the revision being used before overriding a method. Its call order is the relevant contract.

## Composition still matters

A custom stage should coordinate rather than become a collection of unrelated node loops. If an action is reusable across stages or cases, implement it as a Process and place it in Parameters. The stage is appropriate when the behavior needs stage-wide state or must connect several components.

## Multi-stage and coupled thinking

More advanced workflows may:

- run several AnalysisStages sequentially with transferred state;
- define a coupled PythonSolver containing subsolvers;
- alternate subsolver steps until coupling convergence;
- remesh and replace elements during a stage;
- save and restart with serialized model/solver/process state.

The same separation remains: the stage owns “when,” the solver owns “how the physics is solved,” and elements/conditions own local equations.

## Work through these changes

1. Pass `area_scale` from a new top-level Parameters block instead of a Python argument.
2. Override `KeepAdvancingSolutionLoop` to stop when displacement reaches a threshold; use a ramped load case.
3. Record total reaction over a support submodelpart rather than a single node.
4. Add elapsed wall-clock timing around each solve without altering the solver.
5. Move the monitoring behavior into a Process and compare the stage and process versions.
6. Add a unit test showing that a non-positive `area_scale` is rejected before solver construction.

Next: [Chapter 09 — Heat diffusion](../09_heat_diffusion/README.md).
