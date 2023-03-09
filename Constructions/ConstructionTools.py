import openstudio
from openstudio.openstudiomodel import StandardOpaqueMaterial, MaterialVector, Construction
from openstudio.openstudiomodel import MasslessOpaqueMaterial, SimpleGlazing


class ConstructionTool:

    @staticmethod
    def opaque_standard(
            model: openstudio.openstudiomodel.Model,
            name,
            thickness=None,
            conductivity=None,
            density=None,
            specific_heat=None,
            roughness: str = None):

        mat = StandardOpaqueMaterial(model)
        mat.setName(name)
        if thickness is not None: mat.setThickness(thickness)
        if conductivity is not None: mat.setConductivity(conductivity)
        if density is not None: mat.setDensity(density)
        if specific_heat is not None: mat.setSpecificHeat(specific_heat)
        if roughness is not None: mat.setRoughness(roughness)

        return mat

    # Opaque construction
    @staticmethod
    def opaque_no_mass(model, name, thermal_resistance, roughness="MediumRough"):
        mat = MasslessOpaqueMaterial(model, roughness, thermal_resistance)
        mat.setName(name)

        mat_vec = MaterialVector()
        mat_vec.append(mat)

        cons = Construction(model)
        cons.setName(name)
        cons.setLayers(mat_vec)

        return cons

    # Simple Glazing
    @staticmethod
    def simple_glazing(model, name, u_factor, shgc, tv):
        mat = SimpleGlazing(model, u_factor, shgc)
        mat.setName(name)
        mat.setVisibleTransmittance(tv)

        mat_vec = MaterialVector()
        mat_vec.append(mat)

        cons = Construction(model)
        cons.setName(name)
        cons.setLayers(mat_vec)

        return cons
