# Sources and version policy

The guide follows Kratos's public Python interface and the architecture documented in the main Kratos repository. The examples are original, small verification cases. They do not copy external example code.

## Source files to read in a Kratos checkout

The Python implementation is part of the interface documentation. These files define the lifecycle and defaults used throughout the guide:

- `kratos/python_scripts/analysis_stage.py`
- `kratos/python_scripts/python_solver.py`
- `kratos/python_scripts/process_factory.py`
- `kratos/python_scripts/model_parameters_factory.py`
- `kratos/python_scripts/project.py`
- `kratos/python_scripts/orchestrators/orchestrator.py`
- `kratos/python_scripts/orchestrators/sequential_orchestrator.py`
- `kratos/python_scripts/vtk_output_process.py`
- `applications/StructuralMechanicsApplication/python_scripts/structural_mechanics_analysis.py`
- `applications/StructuralMechanicsApplication/python_scripts/structural_mechanics_solver.py`
- `applications/ConvectionDiffusionApplication/python_scripts/convection_diffusion_analysis.py`
- `applications/ConvectionDiffusionApplication/python_scripts/convection_diffusion_solver.py`

Installed packages may place these modules directly under `KratosMultiphysics/`. The source-tree paths above are preferable in repository documentation because they do not depend on a packaging layout.

## Official documentation

- [Kratos repository](https://github.com/KratosMultiphysics/Kratos)
- [Kratos documentation](https://kratosmultiphysics.github.io/Kratos/)
- [Kratos basics](https://kratosmultiphysics.github.io/Kratos/pages/Kratos/For_Users/Crash_Course/2_Basics.html)
- [ModelPart and SubModelPart](https://kratosmultiphysics.github.io/Kratos/pages/Kratos/For_Users/Crash_Course/Data_Structure/Modelpart_And_Submodelpart.html)
- [Nodes and nodal data](https://kratosmultiphysics.github.io/Kratos/pages/Kratos/For_Users/Crash_Course/Data_Structure/Nodes_And_Data)
- [Elements and conditions](https://kratosmultiphysics.github.io/Kratos/pages/Kratos/For_Users/Crash_Course/Data_Structure/Elems_And_Conds.html)
- [MDPA input format](https://kratosmultiphysics.github.io/Kratos/pages/Kratos/For_Users/Crash_Course/Input_Output_and_Visualization/Input_Data.html)
- [Reading a ModelPart](https://kratosmultiphysics.github.io/Kratos/pages/Kratos/For_Users/Crash_Course/Input_Output_and_Visualization/Reading_Input)
- [Project Parameters](https://kratosmultiphysics.github.io/Kratos/pages/Kratos/For_Users/Crash_Course/Input_Output_and_Visualization/Project_Parameters.html)
- [AnalysisStage and simulation loop](https://kratosmultiphysics.github.io/Kratos/pages/Kratos/For_Users/Crash_Course/5_Simulation_Loop.html)
- [Common Python interface](https://kratosmultiphysics.github.io/Kratos/pages/Kratos/For_Developers/Applications/Common_Python_Interface.html)
- [Solving strategies](https://kratosmultiphysics.github.io/Kratos/pages/Kratos/For_Developers/Solvers/Solving_Strategies.html)
- [Using processes](https://kratosmultiphysics.github.io/Kratos/pages/Kratos/For_Users/Tutorials/Using_Processes.html)
- [Registry architecture](https://kratosmultiphysics.github.io/Kratos/pages/Kratos/For_Developers/General/Registry.html)
- [Creating elements](https://kratosmultiphysics.github.io/Kratos/pages/Kratos/For_Developers/Tutorials/Creating_Elements.html)
- [Kratos examples repository](https://github.com/KratosMultiphysics/Examples)
- [Kratos FlowGraph repository](https://github.com/KratosMultiphysics/Flowgraph)
- [Kratos FlowGraph documentation](https://kratosmultiphysics.github.io/Flowgraph/)

The FlowGraph appendix was checked against the repository implementation as well as its user documentation. FlowGraph evolves independently from Kratos; use the node definitions from the exact FlowGraph revision being run and validate every generated case with the target Kratos revision.

## Differences between Kratos versions

Component names, defaults, configuration schemas, and factory mechanisms evolve. When using another revision:

1. use the Python interpreter and modules produced by that build;
2. inspect the selected solver's `GetDefaultParameters()`;
3. inspect an element's `GetSpecifications()` where available;
4. confirm that required Applications and components are registered;
5. read the analysis, solver, and process factory from the same checkout;
6. run the analytical verification cases before transferring a larger model.

A snippet from another release is evidence, not authority. The source, tests, and defaults from the revision being run determine its interface.
