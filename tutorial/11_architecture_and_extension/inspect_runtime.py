"""Inspect the variable and factory registries populated by imported applications."""

from __future__ import annotations

import KratosMultiphysics as KM
import KratosMultiphysics.ConvectionDiffusionApplication  # noqa: F401
import KratosMultiphysics.StructuralMechanicsApplication  # noqa: F401


def main() -> None:
    for variable_name in ("TEMPERATURE", "DISPLACEMENT", "POINT_LOAD", "CROSS_AREA"):
        print(
            f"{variable_name:14} registered={KM.KratosGlobals.HasVariable(variable_name)!s:5} "
            f"type={KM.KratosGlobals.GetVariableType(variable_name)}"
        )

    process_names, _ = KM.Registry.keys("Processes.KratosMultiphysics")
    selected = sorted(name for name in process_names if "Variable" in name)[:12]
    print("\nSelected registered core processes:")
    for name in selected:
        print(f"  Processes.KratosMultiphysics.{name}")

    registry_path = "Processes.KratosMultiphysics.AssignScalarVariableProcess"
    print(f"\nFactory path exists: {registry_path} -> {KM.Registry.HasItem(registry_path)}")


if __name__ == "__main__":
    main()
