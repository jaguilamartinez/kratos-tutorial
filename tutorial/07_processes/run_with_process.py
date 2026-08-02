"""Run the truss with a user-defined time-dependent load process."""

from __future__ import annotations

from pathlib import Path

import KratosMultiphysics as KM
from KratosMultiphysics.StructuralMechanicsApplication.structural_mechanics_analysis import (
    StructuralMechanicsAnalysis,
)


CASE_DIR = Path(__file__).resolve().parent / "case"


def main() -> None:
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

    model = KM.Model()
    StructuralMechanicsAnalysis(model, parameters).Run()

    final_displacement = model["Structure"].GetNode(2).GetSolutionStepValue(
        KM.DISPLACEMENT_X
    )
    expected = 1000.0 * 1.0 / (210.0e9 * 0.01)
    assert abs(final_displacement - expected) < 1.0e-12


if __name__ == "__main__":
    main()
