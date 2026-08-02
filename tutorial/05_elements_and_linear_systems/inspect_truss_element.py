"""Ask a real Kratos element for its local finite-element equations."""

from __future__ import annotations

import KratosMultiphysics as KM
import KratosMultiphysics.StructuralMechanicsApplication as SMA


def main() -> None:
    model = KM.Model()
    model_part = model.CreateModelPart("Structure")
    model_part.ProcessInfo[KM.DOMAIN_SIZE] = 3
    model_part.AddNodalSolutionStepVariable(KM.DISPLACEMENT)
    model_part.AddNodalSolutionStepVariable(KM.REACTION)

    for node_id, x in ((1, 0.0), (2, 1.0)):
        node = model_part.CreateNewNode(node_id, x, 0.0, 0.0)
        node.AddDof(KM.DISPLACEMENT_X, KM.REACTION_X)
        node.AddDof(KM.DISPLACEMENT_Y, KM.REACTION_Y)
        node.AddDof(KM.DISPLACEMENT_Z, KM.REACTION_Z)

    properties = model_part.CreateNewProperties(1)
    properties[KM.YOUNG_MODULUS] = 210.0e9
    properties[SMA.CROSS_AREA] = 0.01
    properties[KM.DENSITY] = 7850.0
    properties[KM.CONSTITUTIVE_LAW] = SMA.TrussConstitutiveLaw()

    element = model_part.CreateNewElement(
        "TrussLinearElement3D2N", 1, [1, 2], properties
    )
    element.Initialize(model_part.ProcessInfo)

    lhs = KM.Matrix()
    rhs = KM.Vector()
    element.CalculateLocalSystem(lhs, rhs, model_part.ProcessInfo)

    print("Required/produced data declared by the element:")
    print(element.GetSpecifications().PrettyPrintJsonString())
    print("Local stiffness matrix K_e (DOF order x1,y1,z1,x2,y2,z2):")
    print(lhs)
    print("Local residual/right-hand side r_e:")
    print(rhs)

    axial_stiffness = 210.0e9 * 0.01 / 1.0
    assert abs(lhs[0, 0] - axial_stiffness) < 1.0e-6
    assert abs(lhs[0, 3] + axial_stiffness) < 1.0e-6


if __name__ == "__main__":
    main()
