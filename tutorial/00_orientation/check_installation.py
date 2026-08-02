"""Report the Python runtime and Kratos components used by the examples."""

from __future__ import annotations

import platform
import sys

import KratosMultiphysics as KM
import KratosMultiphysics.ConvectionDiffusionApplication as CDA
import KratosMultiphysics.StructuralMechanicsApplication as SMA


def main() -> None:
    print(f"Python executable : {sys.executable}")
    print(f"Python version    : {platform.python_version()}")
    print(f"Machine           : {platform.machine()}")
    print(f"Kratos module     : {KM.__file__}")
    print(f"Kratos version    : {KM.Kernel.Version()}")
    print(f"Distributed run   : {KM.IsDistributedRun()}")
    print(f"Threads           : {KM.ParallelUtilities.GetNumThreads()}")
    print(f"Structural module : {SMA.__file__}")
    print(f"Thermal module    : {CDA.__file__}")


if __name__ == "__main__":
    main()
