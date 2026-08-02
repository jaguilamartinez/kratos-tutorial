"""Read, query, validate, and safely extend Kratos Parameters."""

from __future__ import annotations

from pathlib import Path

import KratosMultiphysics as KM


HERE = Path(__file__).resolve().parent


def main() -> None:
    settings = KM.Parameters((HERE / "settings.json").read_text(encoding="utf-8"))
    solver_settings = settings["solver_settings"]

    defaults = KM.Parameters(
        r"""
        {
            "solver_type": "static",
            "echo_level": 0,
            "compute_reactions": true,
            "time_stepping": {"time_step": 1.0}
        }
        """
    )
    solver_settings.ValidateAndAssignDefaults(defaults)

    time_step = solver_settings["time_stepping"]["time_step"].GetDouble()
    loads = [settings["loads"][i].GetDouble() for i in range(settings["loads"].size())]
    solver_settings["echo_level"].SetInt(2)

    print(f"Solver type       : {solver_settings['solver_type'].GetString()}")
    print(f"Time step         : {time_step}")
    print(f"Loads             : {loads}")
    print(f"Default inserted  : {solver_settings['compute_reactions'].GetBool()}")
    print(f"Updated echo level: {solver_settings['echo_level'].GetInt()}")
    print("\nValidated configuration:")
    print(settings.PrettyPrintJsonString())


if __name__ == "__main__":
    main()
