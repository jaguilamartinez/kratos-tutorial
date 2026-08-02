"""A user-defined Kratos process that ramps POINT_LOAD and monitors response."""

from __future__ import annotations

import KratosMultiphysics as KM
import KratosMultiphysics.StructuralMechanicsApplication as SMA


def Factory(settings: KM.Parameters, model: KM.Model) -> "RampLoadProcess":
    """Required entry point used by KratosProcessFactory."""
    if not isinstance(settings, KM.Parameters):
        raise TypeError("Expected a Kratos Parameters object")
    return RampLoadProcess(model, settings["Parameters"])


class RampLoadProcess(KM.Process):
    def __init__(self, model: KM.Model, settings: KM.Parameters) -> None:
        super().__init__()
        defaults = KM.Parameters(
            r"""
            {
                "model_part_name": "Structure.LoadPoint",
                "start_load": 0.0,
                "end_load": 1.0,
                "interval": [0.0, 1.0]
            }
            """
        )
        settings.ValidateAndAssignDefaults(defaults)

        self.model_part = model[settings["model_part_name"].GetString()]
        self.start_load = settings["start_load"].GetDouble()
        self.end_load = settings["end_load"].GetDouble()
        self.start_time = settings["interval"][0].GetDouble()
        self.end_time = settings["interval"][1].GetDouble()
        if self.end_time <= self.start_time:
            raise ValueError("'interval' must have strictly increasing start and end times")

    def Check(self) -> int:
        if self.model_part.NumberOfNodes() == 0:
            raise RuntimeError(f"ModelPart '{self.model_part.FullName()}' contains no nodes")
        root_model_part = self.model_part.GetRootModelPart()
        if not root_model_part.HasNodalSolutionStepVariable(SMA.POINT_LOAD):
            raise RuntimeError("POINT_LOAD is not allocated as nodal solution-step data")
        return 0

    def _load_at(self, time: float) -> float:
        if time <= self.start_time:
            return self.start_load
        if time >= self.end_time:
            return self.end_load
        fraction = (time - self.start_time) / (self.end_time - self.start_time)
        return self.start_load + fraction * (self.end_load - self.start_load)

    def ExecuteInitializeSolutionStep(self) -> None:
        time = self.model_part.ProcessInfo[KM.TIME]
        load = self._load_at(time)
        value = KM.Array3()
        value[0], value[1], value[2] = load, 0.0, 0.0
        for node in self.model_part.Nodes:
            node.SetSolutionStepValue(SMA.POINT_LOAD, 0, value)

    def ExecuteFinalizeSolutionStep(self) -> None:
        time = self.model_part.ProcessInfo[KM.TIME]
        node = next(iter(self.model_part.Nodes))
        load = node.GetSolutionStepValue(SMA.POINT_LOAD_X)
        displacement = node.GetSolutionStepValue(KM.DISPLACEMENT_X)
        print(f"process monitor | time={time:.1f} load={load:7.2f} N ux={displacement:.6e} m")
