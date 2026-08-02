"""Summarize the structure and file references of a Kratos ProjectParameters file.

This is intentionally a structural inspector. A real validity check requires constructing
the selected Kratos components and, ultimately, running a verified case.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterator

import KratosMultiphysics as KM


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_FILE = (
    ROOT
    / "tutorial"
    / "06_complete_structural_analysis"
    / "case"
    / "ProjectParameters.json"
)


def read_parameters(path: Path) -> KM.Parameters:
    return KM.Parameters(path.read_text(encoding="utf-8"))


def stage_settings(
    parameters: KM.Parameters,
) -> Iterator[tuple[str, KM.Parameters]]:
    is_multistage = parameters.Has("orchestrator") and parameters.Has("stages")
    if is_multistage:
        for name, stage in parameters["stages"].items():
            if not stage.Has("stage_settings"):
                raise ValueError(f"stage '{name}' has no 'stage_settings' block")
            yield name, stage["stage_settings"]
    else:
        yield "single_stage", parameters


def optional_string(parameters: KM.Parameters, key: str, fallback: str = "<absent>") -> str:
    if parameters.Has(key) and parameters[key].IsString():
        return parameters[key].GetString()
    return fallback


def resolve_input_path(
    settings: KM.Parameters, key: str, base_dir: Path, suffix: str = ""
) -> tuple[Path, bool] | None:
    if not settings.Has(key) or not settings[key].IsString():
        return None

    raw_text = settings[key].GetString()
    if raw_text == "":
        return None
    raw = Path(raw_text)
    candidate = raw if raw.is_absolute() else base_dir / raw
    if suffix and candidate.suffix == "":
        candidate = candidate.with_suffix(suffix)
    candidate = candidate.resolve()
    return candidate, candidate.exists()


def print_processes(stage: KM.Parameters) -> None:
    for block_name in ("processes", "output_processes"):
        if not stage.Has(block_name):
            print(f"  {block_name}: <absent>")
            continue

        groups = stage[block_name]
        print(f"  {block_name}:")
        for group_name, descriptors in groups.items():
            print(f"    {group_name}: {descriptors.size()} item(s)")
            for index in range(descriptors.size()):
                descriptor = descriptors[index]
                if descriptor.Has("name"):
                    consumer = descriptor["name"].GetString()
                else:
                    module = optional_string(descriptor, "kratos_module", "user module")
                    script = optional_string(descriptor, "python_module")
                    consumer = f"{module}.{script}"
                print(f"      [{index}] {consumer}")


def print_file_references(stage: KM.Parameters, base_dir: Path) -> None:
    if not stage.Has("solver_settings"):
        return

    solver = stage["solver_settings"]
    references: list[tuple[str, tuple[Path, bool] | None]] = []

    if solver.Has("model_import_settings"):
        model_import = solver["model_import_settings"]
        input_type = optional_string(model_import, "input_type", "unknown")
        references.append(
            (
                f"model input ({input_type})",
                resolve_input_path(
                    model_import,
                    "input_filename",
                    base_dir,
                    suffix=".mdpa" if input_type == "mdpa" else "",
                ),
            )
        )
    if solver.Has("material_import_settings"):
        references.append(
            (
                "materials",
                resolve_input_path(
                    solver["material_import_settings"],
                    "materials_filename",
                    base_dir,
                ),
            )
        )

    print("  candidate input paths (resolved relative to this JSON for review):")
    for label, result in references:
        if result is None:
            print(f"    {label}: <not a string path>")
            continue
        path, exists = result
        print(f"    {label}: {path} ({'exists' if exists else 'missing'})")


def print_stage(name: str, stage: KM.Parameters, base_dir: Path) -> None:
    print(f"\nStage: {name}")
    print(f"  analysis_stage: {optional_string(stage, 'analysis_stage')}")

    if stage.Has("problem_data"):
        problem = stage["problem_data"]
        print(f"  problem_name: {optional_string(problem, 'problem_name')}")
        print(f"  parallel_type: {optional_string(problem, 'parallel_type')}")
        if problem.Has("start_time") and problem.Has("end_time"):
            print(
                "  time interval: "
                f"[{problem['start_time'].GetDouble()}, {problem['end_time'].GetDouble()}]"
            )
    else:
        print("  problem_data: <absent>")

    if stage.Has("solver_settings"):
        solver = stage["solver_settings"]
        print(f"  solver_type: {optional_string(solver, 'solver_type')}")
        print(f"  model_part_name: {optional_string(solver, 'model_part_name')}")
        if solver.Has("domain_size"):
            domain_size = solver["domain_size"]
            value = domain_size.GetInt() if domain_size.IsInt() else domain_size.WriteJsonString()
            print(f"  domain_size: {value}")
    else:
        print("  solver_settings: <absent>")

    print_processes(stage)
    print_file_references(stage, base_dir)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "project_parameters",
        nargs="?",
        type=Path,
        default=DEFAULT_FILE,
        help="file to inspect (defaults to the tutorial's linear truss case)",
    )
    args = parser.parse_args()

    path = args.project_parameters.expanduser().resolve()
    parameters = read_parameters(path)
    is_multistage = parameters.Has("orchestrator") and parameters.Has("stages")

    print(f"File: {path}")
    print(f"Layout: {'multistage' if is_multistage else 'conventional single-stage'}")
    if is_multistage:
        orchestrator = parameters["orchestrator"]
        print(f"Orchestrator: {optional_string(orchestrator, 'name')}")
        if orchestrator.Has("settings") and orchestrator["settings"].Has("execution_list"):
            execution_list = orchestrator["settings"]["execution_list"].GetStringArray()
            print(f"Execution list: {execution_list}")

    count = 0
    for name, stage in stage_settings(parameters):
        print_stage(name, stage, path.parent)
        count += 1

    if count == 0:
        raise RuntimeError("no stages found")
    print(f"\nInspected {count} stage(s).")


if __name__ == "__main__":
    main()
