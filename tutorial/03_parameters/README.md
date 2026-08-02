# Chapter 03 — Typed configuration with `Parameters`

Kratos uses `Parameters` to pass configuration through solvers, processes, modelers, and output. It is a typed, mutable view of JSON data. Correct use of it catches misspelled options and wrong types before the numerical solve begins.

## Run the example

```bash
python3 tutorial/03_parameters/parameters.py
```

## Why not pass raw dictionaries everywhere?

`KM.Parameters` is a thin typed wrapper around JSON. A consumer asks explicitly for a type:

```python
echo_level = settings["echo_level"].GetInt()
time_step = settings["time_stepping"]["time_step"].GetDouble()
solver_type = settings["solver_type"].GetString()
```

This moves many configuration mistakes to initialization. A string where an integer is expected produces a clear failure rather than flowing deep into a numerical calculation.

JSON supports objects, arrays, strings, numbers, booleans, and null. It does not support comments or Python expressions. Some Kratos process settings deliberately accept expression **strings**, but those are interpreted by that process and are not general JSON expressions.

## Defaults and validation

A well-designed Kratos component publishes defaults:

```python
defaults = KM.Parameters(r'''{
    "echo_level": 0,
    "compute_reactions": true
}''')
settings.ValidateAndAssignDefaults(defaults)
```

This operation:

- checks user-provided keys and types at the current object level;
- inserts missing values at that level;
- rejects unexpected keys at that level.

`ValidateAndAssignDefaults` is deliberately shallow. A nested object is treated as one value unless the component validates it separately. Use `RecursivelyValidateAndAssignDefaults` only when the entire nested tree belongs to the same schema and should be checked recursively. Kratos solvers commonly validate their top level and then validate selected sub-blocks with the component that owns them.

Do not blindly suppress an “unexpected parameter” error. It often identifies an option from another Kratos version, another application, or the wrong nesting level.

## Views and mutation

Indexing normally returns a view into the same Parameters tree:

```python
solver_settings = settings["solver_settings"]
solver_settings["echo_level"].SetInt(2)
```

The original `settings` now contains `2`. This behavior is useful for programmatic studies but can surprise code expecting an independent copy. Use `Clone()` when independent settings are required.

The capstone creates fresh Parameters for each solve before modifying a load. That prevents a process or validation routine from leaving mutations that affect the next case.

## Arrays

Kratos Parameters arrays use `size()` and integer indexing:

```python
for i in range(settings["loads"].size()):
    load = settings["loads"][i].GetDouble()
```

Several convenience functions exist for homogeneous arrays, but explicit indexing makes types and mutations easy to see while learning.

## Configuration layout

Complete cases commonly separate:

- `problem_data`: run name, time span, parallel type, logging;
- `solver_settings`: physics and numerical algorithm;
- `processes`: constraints, loads, initialization, monitoring;
- `output_processes`: scheduled output;
- material settings and mesh filenames.

The application AnalysisStage selects the solver from `solver_settings`; the solver validates its own settings; process factories construct behavior from the process lists.

## Configuration discipline

- Keep case-specific numerical choices in input files rather than modifying library code.
- Put units in documentation and parameter names where ambiguity is possible.
- Archive the fully expanded/validated settings for important runs.
- Change one parameter at a time in diagnosis.
- Generate sweeps from a pristine base configuration.
- Prefer defaults from the revision being run over settings copied from another release.

## Work through these changes

1. Change `time_step` to a string and interpret the resulting typed-access failure.
2. Add an unknown solver key and observe validation behavior.
3. Call `Clone()`, change the clone's echo level, and prove the original is unchanged.
4. Add a nested convergence block with relative and absolute tolerances and a matching default schema.
5. Write a small function that accepts Parameters, validates it, and returns a dimensional load vector.

Next: [Chapter 04 — MDPA input](../04_mdpa_io/README.md).

For the complete configuration model, continue with [Appendix A — ProjectParameters in depth](../../appendices/A_project_parameters/README.md).
