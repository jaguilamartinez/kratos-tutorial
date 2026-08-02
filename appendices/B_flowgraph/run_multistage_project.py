"""Run and verify a sequential multistage ProjectParameters configuration."""

from __future__ import annotations

from pathlib import Path

import KratosMultiphysics as KM
from KratosMultiphysics.orchestrators.sequential_orchestrator import (
    SequentialOrchestrator,
)
from KratosMultiphysics.project import Project


CASE_DIR = Path(__file__).resolve().parent / "case"
FORCE = 1_000.0
LENGTH = 1.0
YOUNG_MODULUS = 210.0e9
AREA = 0.01


def read_parameters() -> KM.Parameters:
    parameters = KM.Parameters(
        (CASE_DIR / "ProjectParameters.json").read_text(encoding="utf-8")
    )
    stage = parameters["stages"]["one_bar"]["stage_settings"]
    solver = stage["solver_settings"]
    solver["model_import_settings"]["input_filename"].SetString(
        str(CASE_DIR / "truss")
    )
    solver["material_import_settings"]["materials_filename"].SetString(
        str(CASE_DIR / "Materials.json")
    )
    return parameters


def main() -> None:
    project = Project(read_parameters())
    orchestrator = SequentialOrchestrator(project)
    orchestrator.Run()

    structure = project.GetModel()["Structure"]
    displacement = structure.GetNode(2).GetSolutionStepValue(KM.DISPLACEMENT_X)
    reaction = structure.GetNode(1).GetSolutionStepValue(KM.REACTION_X)
    expected_displacement = FORCE * LENGTH / (YOUNG_MODULUS * AREA)

    print("\nMultistage verification")
    print(f"  executed stages     : {list(project.GetOutputData())}")
    print(f"  Kratos displacement : {displacement:.12e} m")
    print(f"  analytical F L / EA : {expected_displacement:.12e} m")
    print(f"  support reaction    : {reaction:.6f} N")

    if abs(displacement - expected_displacement) > 1.0e-12:
        raise RuntimeError("the multistage result does not match F L / (E A)")
    if abs(reaction + FORCE) > 1.0e-8:
        raise RuntimeError("the support reaction does not balance the applied load")
    if list(project.GetOutputData()) != ["one_bar"]:
        raise RuntimeError("the sequential orchestrator executed an unexpected stage list")


if __name__ == "__main__":
    main()
