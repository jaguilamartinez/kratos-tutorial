"""Customize orchestration safely by deriving from an application's AnalysisStage."""

from __future__ import annotations

from pathlib import Path

import KratosMultiphysics as KM
import KratosMultiphysics.StructuralMechanicsApplication as SMA
from KratosMultiphysics.StructuralMechanicsApplication.structural_mechanics_analysis import (
    StructuralMechanicsAnalysis,
)


STRUCTURAL_CASE = (
    Path(__file__).resolve().parents[1] / "06_complete_structural_analysis" / "case"
)


class MonitoringStructuralAnalysis(StructuralMechanicsAnalysis):
    def __init__(self, model: KM.Model, parameters: KM.Parameters, area_scale: float) -> None:
        if area_scale <= 0.0:
            raise ValueError("area_scale must be positive")
        self.area_scale = area_scale
        self.history: list[dict[str, float]] = []
        super().__init__(model, parameters)

    def ModifyInitialProperties(self) -> None:
        """Hook called after model/material import and before solver initialization."""
        properties = self.model["Structure"].GetProperties()[1]
        properties[SMA.CROSS_AREA] *= self.area_scale

    def FinalizeSolutionStep(self) -> None:
        """Preserve base behavior, then add application-specific monitoring."""
        super().FinalizeSolutionStep()
        model_part = self.model["Structure"]
        self.history.append(
            {
                "time": model_part.ProcessInfo[KM.TIME],
                "tip_displacement": model_part.GetNode(2).GetSolutionStepValue(
                    KM.DISPLACEMENT_X
                ),
                "support_reaction": model_part.GetNode(1).GetSolutionStepValue(
                    KM.REACTION_X
                ),
            }
        )

    def GetFinalData(self) -> dict[str, float]:
        return self.history[-1] if self.history else {}


def main() -> None:
    parameters = KM.Parameters(
        (STRUCTURAL_CASE / "ProjectParameters.json").read_text(encoding="utf-8")
    )
    solver_settings = parameters["solver_settings"]
    solver_settings["model_import_settings"]["input_filename"].SetString(
        str(STRUCTURAL_CASE / "truss")
    )
    solver_settings["material_import_settings"]["materials_filename"].SetString(
        str(STRUCTURAL_CASE / "Materials.json")
    )

    model = KM.Model()
    analysis = MonitoringStructuralAnalysis(model, parameters, area_scale=2.0)
    analysis.Run()
    result = analysis.GetFinalData()

    expected = 1000.0 * 1.0 / (210.0e9 * (2.0 * 0.01))
    print(f"Custom-stage result : {result}")
    print(f"Expected tip ux     : {expected:.12e} m")
    assert abs(result["tip_displacement"] - expected) < 1.0e-12


if __name__ == "__main__":
    main()
