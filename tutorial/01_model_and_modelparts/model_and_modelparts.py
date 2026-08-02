"""Build a small mesh in memory and explore Kratos ownership semantics."""

from __future__ import annotations

import KratosMultiphysics as KM


def main() -> None:
    model = KM.Model()
    domain = model.CreateModelPart("Domain")
    domain.ProcessInfo[KM.DOMAIN_SIZE] = 2

    # Root ModelParts own entities. SubModelParts provide overlapping views/groups.
    boundary = domain.CreateSubModelPart("Boundary")
    inlet = boundary.CreateSubModelPart("Inlet")
    fluid = domain.CreateSubModelPart("Fluid")

    domain.CreateNewNode(1, 0.0, 0.0, 0.0)
    domain.CreateNewNode(2, 1.0, 0.0, 0.0)
    domain.CreateNewNode(3, 0.0, 1.0, 0.0)

    properties = domain.CreateNewProperties(1)
    element = domain.CreateNewElement("Element2D3N", 1, [1, 2, 3], properties)
    condition = domain.CreateNewCondition("LineCondition2D2N", 1, [1, 3], properties)

    # Add existing root-owned entities to groups by ID.
    fluid.AddNodes([1, 2, 3])
    fluid.AddElements([1])
    inlet.AddNodes([1, 3])
    inlet.AddConditions([1])

    print(f"Model contains Domain: {model.HasModelPart('Domain')}")
    print(f"Root nodes            : {[node.Id for node in domain.Nodes]}")
    print(f"Inlet nodes           : {[node.Id for node in inlet.Nodes]}")
    print(f"Fluid elements        : {[item.Id for item in fluid.Elements]}")
    print(f"Triangle area          : {element.GetGeometry().Area():.3f}")
    print(f"Boundary length        : {condition.GetGeometry().Length():.3f}")
    print(f"Nested lookup          : {model['Domain.Boundary.Inlet'].FullName()}")

    # The same node object is visible through both containers.
    assert domain.GetNode(1).Id == inlet.GetNode(1).Id
    assert domain.NumberOfNodes() == 3
    assert inlet.NumberOfNodes() == 2


if __name__ == "__main__":
    main()
