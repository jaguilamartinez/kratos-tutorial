"""Solve a stationary 2D heat equation and verify the linear exact solution."""

from __future__ import annotations

from pathlib import Path

import KratosMultiphysics as KM
from KratosMultiphysics.ConvectionDiffusionApplication.convection_diffusion_analysis import (
    ConvectionDiffusionAnalysis,
)


CASE_DIR = Path(__file__).resolve().parent / "case"


def main() -> None:
    parameters = KM.Parameters(
        (CASE_DIR / "ProjectParameters.json").read_text(encoding="utf-8")
    )
    solver_settings = parameters["solver_settings"]
    solver_settings["model_import_settings"]["input_filename"].SetString(
        str(CASE_DIR / "square")
    )
    solver_settings["material_import_settings"]["materials_filename"].SetString(
        str(CASE_DIR / "Materials.json")
    )

    model = KM.Model()
    ConvectionDiffusionAnalysis(model, parameters).Run()

    thermal_domain = model["ThermalDomain"]
    print("\nNodal solution (exact field is T = 100 x):")
    for node in thermal_domain.Nodes:
        temperature = node.GetSolutionStepValue(KM.TEMPERATURE)
        expected = 100.0 * node.X
        print(f"  node {node.Id}: x={node.X:.1f}, T={temperature:8.4f}, exact={expected:8.4f}")
        assert abs(temperature - expected) < 1.0e-10


if __name__ == "__main__":
    main()
