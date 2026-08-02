"""Run and verify a one-element 3D truss through StructuralMechanicsAnalysis."""

from __future__ import annotations

from pathlib import Path

import KratosMultiphysics as KM
from KratosMultiphysics.StructuralMechanicsApplication.structural_mechanics_analysis import (
    StructuralMechanicsAnalysis,
)


CASE_DIR = Path(__file__).resolve().parent / "case"
FORCE = 1_000.0
LENGTH = 1.0
YOUNG_MODULUS = 210.0e9
AREA = 0.01


def read_parameters() -> KM.Parameters:
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
    return parameters


def main() -> None:
    model = KM.Model()
    analysis = StructuralMechanicsAnalysis(model, read_parameters())
    analysis.Run()

    structure = model["Structure"]
    displacement = structure.GetNode(2).GetSolutionStepValue(KM.DISPLACEMENT_X)
    reaction = structure.GetNode(1).GetSolutionStepValue(KM.REACTION_X)
    expected_displacement = FORCE * LENGTH / (YOUNG_MODULUS * AREA)

    print("\nVerification")
    print(f"  Kratos displacement : {displacement:.12e} m")
    print(f"  Analytical F L / EA : {expected_displacement:.12e} m")
    print(f"  Support reaction    : {reaction:.6f} N")

    if abs(displacement - expected_displacement) > 1.0e-12:
        raise RuntimeError("The finite-element result does not match F L / (E A)")
    if abs(reaction + FORCE) > 1.0e-8:
        raise RuntimeError("The support reaction does not balance the applied load")


if __name__ == "__main__":
    main()
