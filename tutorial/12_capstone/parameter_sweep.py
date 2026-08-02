"""Run a small load sweep as a reproducible simulation experiment."""

from __future__ import annotations

from pathlib import Path

import KratosMultiphysics as KM
from KratosMultiphysics.StructuralMechanicsApplication.structural_mechanics_analysis import (
    StructuralMechanicsAnalysis,
)


CASE_DIR = Path(__file__).resolve().parents[1] / "06_complete_structural_analysis" / "case"


def solve(force: float) -> float:
    parameters = KM.Parameters(
        (CASE_DIR / "ProjectParameters.json").read_text(encoding="utf-8")
    )
    solver_settings = parameters["solver_settings"]
    solver_settings["model_import_settings"]["input_filename"].SetString(
        str(CASE_DIR / "truss")
    )
    solver_settings["material_import_settings"]["materials_filename"].SetString(
        str(CASE_DIR / "Materials.json")
    )
    load_value = parameters["processes"]["loads_process_list"][0]["Parameters"]["value"]
    load_value[0].SetDouble(force)

    model = KM.Model()
    StructuralMechanicsAnalysis(model, parameters).Run()
    return model["Structure"].GetNode(2).GetSolutionStepValue(KM.DISPLACEMENT_X)


def main() -> None:
    forces = (250.0, 500.0, 1000.0, 2000.0)
    results = [(force, solve(force)) for force in forces]

    print("force_N,displacement_m,effective_stiffness_N_per_m")
    for force, displacement in results:
        print(f"{force:.1f},{displacement:.12e},{force / displacement:.6e}")

    expected_stiffness = 210.0e9 * 0.01 / 1.0
    for force, displacement in results:
        assert abs(force / displacement - expected_stiffness) < 1.0e-3


if __name__ == "__main__":
    main()
