"""Read a Kratos MDPA file and inspect the reconstructed object graph."""

from __future__ import annotations

from pathlib import Path

import KratosMultiphysics as KM


MDPA_WITHOUT_EXTENSION = Path(__file__).resolve().parent / "case" / "triangle"


def main() -> None:
    model = KM.Model()
    model_part = model.CreateModelPart("Main")
    model_part.AddNodalSolutionStepVariable(KM.TEMPERATURE)

    KM.ModelPartIO(str(MDPA_WITHOUT_EXTENSION)).ReadModelPart(model_part)

    hot_boundary = model["Main.HotBoundary"]
    temperatures = {
        node.Id: node.GetSolutionStepValue(KM.TEMPERATURE) for node in model_part.Nodes
    }

    print(model_part)
    print(f"Temperatures : {temperatures}")
    print(f"Hot nodes    : {[node.Id for node in hot_boundary.Nodes]}")
    print(f"Element area : {model_part.GetElement(1).GetGeometry().Area():.3f}")

    assert model_part.NumberOfNodes() == 3
    assert temperatures[2] == 50.0


if __name__ == "__main__":
    main()
