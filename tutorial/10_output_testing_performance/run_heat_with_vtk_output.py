"""Attach a VTK OutputProcess to the heat example without changing its case file."""

from __future__ import annotations

from pathlib import Path

import KratosMultiphysics as KM
from KratosMultiphysics.ConvectionDiffusionApplication.convection_diffusion_analysis import (
    ConvectionDiffusionAnalysis,
)


HERE = Path(__file__).resolve().parent
HEAT_CASE = HERE.parent / "09_heat_diffusion" / "case"
OUTPUT_DIR = HERE / "generated" / "vtk"


def main() -> None:
    parameters = KM.Parameters(
        (HEAT_CASE / "ProjectParameters.json").read_text(encoding="utf-8")
    )
    solver_settings = parameters["solver_settings"]
    solver_settings["model_import_settings"]["input_filename"].SetString(
        str(HEAT_CASE / "square")
    )
    solver_settings["material_import_settings"]["materials_filename"].SetString(
        str(HEAT_CASE / "Materials.json")
    )

    vtk_output = KM.Parameters(
        r"""
        {
            "vtk_output": [{
                "python_module": "vtk_output_process",
                "kratos_module": "KratosMultiphysics",
                "Parameters": {
                    "model_part_name": "ThermalDomain",
                    "file_format": "ascii",
                    "output_precision": 10,
                    "output_control_type": "step",
                    "output_interval": 1.0,
                    "output_sub_model_parts": false,
                    "output_path": "placeholder",
                    "save_output_files_in_folder": true,
                    "nodal_solution_step_data_variables": ["TEMPERATURE", "REACTION_FLUX"],
                    "nodal_data_value_variables": ["CONDUCTIVITY"],
                    "element_data_value_variables": [],
                    "condition_data_value_variables": []
                }
            }]
        }
        """
    )
    vtk_output["vtk_output"][0]["Parameters"]["output_path"].SetString(str(OUTPUT_DIR))
    parameters.RemoveValue("output_processes")
    parameters.AddValue("output_processes", vtk_output)

    model = KM.Model()
    ConvectionDiffusionAnalysis(model, parameters).Run()

    output_files = sorted(OUTPUT_DIR.glob("*.vtk"))
    if not output_files:
        raise RuntimeError(f"No VTK file was written to {OUTPUT_DIR}")
    print(f"Wrote {len(output_files)} VTK file(s):")
    for path in output_files:
        print(f"  {path}")


if __name__ == "__main__":
    main()
