"""Integration tests for the complete structural and thermal entry points."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


TUTORIAL_ROOT = Path(__file__).resolve().parents[1]


class TutorialIntegrationTests(unittest.TestCase):
    def run_example(self, relative_path: str, expected_text: str) -> None:
        completed = subprocess.run(
            [sys.executable, str(TUTORIAL_ROOT / relative_path)],
            cwd=TUTORIAL_ROOT.parent,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn(expected_text, completed.stdout)

    def test_structural_truss_matches_closed_form_solution(self) -> None:
        self.run_example(
            "06_complete_structural_analysis/run_analysis.py",
            "Analytical F L / EA",
        )

    def test_heat_problem_matches_linear_exact_field(self) -> None:
        self.run_example(
            "09_heat_diffusion/run_heat_problem.py",
            "exact field is T = 100 x",
        )

    def test_nonlinear_truss_satisfies_finite_deformation_equilibrium(self) -> None:
        self.run_example(
            "06_complete_structural_analysis/run_nonlinear_analysis.py",
            "reconstructed force",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
