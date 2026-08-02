"""Execute every runnable tutorial artifact as a compact smoke-test suite."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent

EXAMPLES = [
    ("00 runtime", ["tutorial/00_orientation/check_installation.py"]),
    ("01 model graph", ["tutorial/01_model_and_modelparts/model_and_modelparts.py"]),
    ("02 variables/time", ["tutorial/02_variables_and_time/variables_and_time.py"]),
    ("03 parameters", ["tutorial/03_parameters/parameters.py"]),
    ("04 MDPA", ["tutorial/04_mdpa_io/read_mdpa.py"]),
    ("05 element local system", ["tutorial/05_elements_and_linear_systems/inspect_truss_element.py"]),
    ("05 assembly", ["tutorial/05_elements_and_linear_systems/assemble_and_solve.py"]),
    ("06 structural analysis", ["tutorial/06_complete_structural_analysis/run_analysis.py"]),
    ("06 nonlinear structural analysis", ["tutorial/06_complete_structural_analysis/run_nonlinear_analysis.py"]),
    ("07 custom process", ["tutorial/07_processes/run_with_process.py"]),
    ("08 custom stage", ["tutorial/08_custom_analysis_stage/monitoring_analysis.py"]),
    ("09 heat diffusion", ["tutorial/09_heat_diffusion/run_heat_problem.py"]),
    ("10 VTK output", ["tutorial/10_output_testing_performance/run_heat_with_vtk_output.py"]),
    ("10 integration tests", ["-m", "unittest", "tutorial/10_output_testing_performance/test_tutorial_cases.py", "-v"]),
    ("10 runtime controls", ["tutorial/10_output_testing_performance/runtime_controls.py"]),
    ("11 runtime registry", ["tutorial/11_architecture_and_extension/inspect_runtime.py"]),
    ("12 capstone sweep", ["tutorial/12_capstone/parameter_sweep.py"]),
    ("A ProjectParameters inspector", ["appendices/A_project_parameters/inspect_project_parameters.py"]),
    ("B multistage project", ["appendices/B_flowgraph/run_multistage_project.py"]),
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", action="store_true", help="print captured program output")
    args = parser.parse_args()

    failures: list[str] = []
    for label, arguments in EXAMPLES:
        completed = subprocess.run(
            [sys.executable, *arguments],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        status = "PASS" if completed.returncode == 0 else "FAIL"
        print(f"[{status}] {label}")
        if args.verbose or completed.returncode != 0:
            print(completed.stdout, end="")
            print(completed.stderr, end="")
        if completed.returncode != 0:
            failures.append(label)

    if failures:
        raise SystemExit(f"{len(failures)} tutorial checks failed: {', '.join(failures)}")
    print(f"\nAll {len(EXAMPLES)} tutorial checks passed.")


if __name__ == "__main__":
    main()
