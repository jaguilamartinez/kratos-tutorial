"""Assemble two scalar springs and solve their global system with Kratos."""

from __future__ import annotations

import KratosMultiphysics as KM
from KratosMultiphysics import python_linear_solver_factory


def add_spring(matrix: KM.CompressedMatrix, node_i: int, node_j: int, stiffness: float) -> None:
    """Assemble k[[1,-1],[-1,1]] into a zero-based global matrix."""
    matrix[node_i, node_i] += stiffness
    matrix[node_i, node_j] -= stiffness
    matrix[node_j, node_i] -= stiffness
    matrix[node_j, node_j] += stiffness


def main() -> None:
    # Nodes 0--1--2, two springs of stiffness 1000 N/m; node 0 is fixed.
    full_matrix = KM.CompressedMatrix(3, 3)
    add_spring(full_matrix, 0, 1, 1000.0)
    add_spring(full_matrix, 1, 2, 1000.0)

    # Eliminate the fixed u0=0 row/column. The free system is K_ff u_f = f_f.
    free_matrix = KM.CompressedMatrix(2, 2)
    for i in range(2):
        for j in range(2):
            free_matrix[i, j] = full_matrix[i + 1, j + 1]

    force = KM.Vector(2)
    force[0] = 0.0
    force[1] = 100.0
    displacement = KM.Vector(2)

    settings = KM.Parameters(r'{"solver_type": "skyline_lu_factorization"}')
    linear_solver = python_linear_solver_factory.ConstructSolver(settings)
    linear_solver.Solve(free_matrix, displacement, force)

    print(f"Global K      : {full_matrix}")
    print(f"Reduced K_ff  : {free_matrix}")
    print(f"Displacements : u1={displacement[0]:.6f}, u2={displacement[1]:.6f} m")
    assert abs(displacement[0] - 0.1) < 1.0e-12
    assert abs(displacement[1] - 0.2) < 1.0e-12


if __name__ == "__main__":
    main()
