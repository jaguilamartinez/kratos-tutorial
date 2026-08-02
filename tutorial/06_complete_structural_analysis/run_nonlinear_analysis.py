"""Solve a finite-deformation truss and verify its nonlinear equilibrium."""

from __future__ import annotations

from pathlib import Path

import KratosMultiphysics as KM
from KratosMultiphysics.StructuralMechanicsApplication.structural_mechanics_analysis import (
    StructuralMechanicsAnalysis,
)


CASE_DIR = Path(__file__).resolve().parent / "case_nonlinear"
FORCE = 1.0e9
YOUNG_MODULUS = 210.0e9
AREA = 0.01
REFERENCE_LENGTH = 1.0


def main() -> None:
    parameters = KM.Parameters(
        (CASE_DIR / "ProjectParameters.json").read_text(encoding="utf-8")
    )
    solver_settings = parameters["solver_settings"]
    solver_settings["model_import_settings"]["input_filename"].SetString(
        str(CASE_DIR / "truss_nonlinear")
    )
    solver_settings["material_import_settings"]["materials_filename"].SetString(
        str(CASE_DIR.parent / "case" / "Materials.json")
    )

    model = KM.Model()
    StructuralMechanicsAnalysis(model, parameters).Run()
    displacement = model["Structure"].GetNode(2).GetSolutionStepValue(KM.DISPLACEMENT_X)

    # The element uses Green-Lagrange strain E_G = (lambda^2-1)/2 and
    # a linear uniaxial material S = E*E_G. Total-Lagrangian equilibrium is
    # F = A*S*lambda. Evaluate that equation at the computed stretch.
    stretch = 1.0 + displacement / REFERENCE_LENGTH
    green_lagrange_strain = 0.5 * (stretch * stretch - 1.0)
    internal_force = AREA * YOUNG_MODULUS * green_lagrange_strain * stretch
    linear_prediction = FORCE * REFERENCE_LENGTH / (YOUNG_MODULUS * AREA)

    print("\nFinite-deformation verification")
    print(f"  nonlinear displacement : {displacement:.9f} m")
    print(f"  small-strain prediction: {linear_prediction:.9f} m")
    print(f"  reconstructed force    : {internal_force:.3f} N")

    if abs(internal_force - FORCE) / FORCE > 1.0e-9:
        raise RuntimeError("The nonlinear truss does not satisfy analytical equilibrium")
    if not displacement < linear_prediction:
        raise RuntimeError("Geometric stiffening was expected for this tensile case")


if __name__ == "__main__":
    main()
