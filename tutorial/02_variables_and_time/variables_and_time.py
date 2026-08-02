"""Contrast historical/non-historical data, DOFs, flags, and the time buffer."""

from __future__ import annotations

import KratosMultiphysics as KM


def main() -> None:
    model = KM.Model()
    model_part = model.CreateModelPart("TransientDomain", 3)

    # Historical variables must be registered before nodes are created/read.
    model_part.AddNodalSolutionStepVariable(KM.TEMPERATURE)
    model_part.AddNodalSolutionStepVariable(KM.VELOCITY)

    node = model_part.CreateNewNode(1, 0.25, 0.50, 0.0)
    node.AddDof(KM.TEMPERATURE)

    model_part.ProcessInfo[KM.STEP] = 0
    model_part.ProcessInfo[KM.TIME] = 0.0
    node.SetSolutionStepValue(KM.TEMPERATURE, 0, 20.0)

    # CloneTimeStep copies the current state to the next step and shifts the buffer.
    for step, (time, temperature) in enumerate(((0.1, 25.0), (0.2, 31.0)), start=1):
        model_part.ProcessInfo[KM.STEP] = step
        model_part.CloneTimeStep(time)
        node.SetSolutionStepValue(KM.TEMPERATURE, 0, temperature)

    # Non-historical data has one value and is independent of the solution-step buffer.
    node.SetValue(KM.NODAL_AREA, 0.125)
    node.Set(KM.ACTIVE, True)
    node.Fix(KM.TEMPERATURE)

    print(f"Current time             : {model_part.ProcessInfo[KM.TIME]:.1f}")
    print(f"T(n) current             : {node.GetSolutionStepValue(KM.TEMPERATURE, 0):.1f}")
    print(f"T(n-1)                   : {node.GetSolutionStepValue(KM.TEMPERATURE, 1):.1f}")
    print(f"T(n-2)                   : {node.GetSolutionStepValue(KM.TEMPERATURE, 2):.1f}")
    print(f"Non-historical NODAL_AREA: {node.GetValue(KM.NODAL_AREA):.3f}")
    print(f"ACTIVE flag              : {node.Is(KM.ACTIVE)}")
    print(f"TEMPERATURE fixed        : {node.IsFixed(KM.TEMPERATURE)}")

    assert [node.GetSolutionStepValue(KM.TEMPERATURE, i) for i in range(3)] == [31.0, 25.0, 20.0]


if __name__ == "__main__":
    main()
