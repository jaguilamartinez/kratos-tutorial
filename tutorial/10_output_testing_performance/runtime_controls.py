"""Inspect process thread controls and time a deterministic Kratos operation."""

from __future__ import annotations

from time import perf_counter

import KratosMultiphysics as KM


def main() -> None:
    original_threads = KM.ParallelUtilities.GetNumThreads()
    chosen_threads = min(4, original_threads)
    KM.ParallelUtilities.SetNumThreads(chosen_threads)

    start = perf_counter()
    model = KM.Model()
    model_part = model.CreateModelPart("TimingDemo")
    for node_id in range(1, 100_001):
        model_part.CreateNewNode(node_id, float(node_id), 0.0, 0.0)
    elapsed = perf_counter() - start

    print(f"Available/configured threads before: {original_threads}")
    print(f"Threads used for this process       : {chosen_threads}")
    print(f"Created {model_part.NumberOfNodes():,} nodes in {elapsed:.3f} s")

    # Restore process-global state so importing this example has no lasting side effect.
    KM.ParallelUtilities.SetNumThreads(original_threads)


if __name__ == "__main__":
    main()
