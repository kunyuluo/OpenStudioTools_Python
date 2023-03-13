import openstudio
from openstudio.openstudiomodel import StandardOpaqueMaterial, MaterialVector, Construction
from openstudio.openstudiomodel import MasslessOpaqueMaterial, SimpleGlazing


class ConstructionTool:

    @staticmethod
    def opaque_standard_material(
            model: openstudio.openstudiomodel.Model,
            name,
            thickness=None,
            conductivity=None,
            density=None,
            specific_heat=None,
            roughness: str = None,
            thermal_absorptance=None,
            solar_absorptance=None,
            visible_absorptance=None):

        mat = StandardOpaqueMaterial(model)
        mat.setName(name)
        if thickness is not None: mat.setThickness(thickness)
        if conductivity is not None: mat.setConductivity(conductivity)
        if density is not None: mat.setDensity(density)
        if specific_heat is not None: mat.setSpecificHeat(specific_heat)
        if roughness is not None: mat.setRoughness(roughness)
        if thermal_absorptance is not None: mat.setThermalAbsorptance(thermal_absorptance)
        if solar_absorptance is not None: mat.setSolarAbsorptance(solar_absorptance)
        if visible_absorptance is not None: mat.setVisibleAbsorptance(visible_absorptance)

        return mat

    @staticmethod
    def construction(model: openstudio.openstudiomodel.Model, name=None):
        cons = openstudio.openstudiomodel.Construction(model)
        if name is not None: cons.setName(name)
        return cons

    @staticmethod
    def opaque_no_mass_material(
            model: openstudio.openstudiomodel.Model,
            name,
            thermal_resistance,
            roughness="MediumRough",
            thermal_absorptance=None,
            solar_absorptance=None,
            visible_absorptance=None):
        mat = MasslessOpaqueMaterial(model, roughness, thermal_resistance)
        mat.setName(name)
        if thermal_absorptance is not None: mat.setThermalAbsorptance(thermal_absorptance)
        if solar_absorptance is not None: mat.setSolarAbsorptance(solar_absorptance)
        if visible_absorptance is not None: mat.setVisibleAbsorptance(visible_absorptance)
        return mat

    # Opaque construction
    @staticmethod
    def opaque_no_mass_cons(model, name, thermal_resistance, roughness="MediumRough"):
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
    def simple_glazing_cons(model, name, u_factor, shgc, tv):
        mat = SimpleGlazing(model, u_factor, shgc)
        mat.setName(name)
        mat.setVisibleTransmittance(tv)

        mat_vec = MaterialVector()
        mat_vec.append(mat)

        cons = Construction(model)
        cons.setName(name)
        cons.setLayers(mat_vec)

        return cons

    @staticmethod
    def air_gap(model, name=None, thermal_resistance=None):
        if thermal_resistance is not None:
            gap = openstudio.openstudiomodel.AirGap(model)
        else:
            gap = openstudio.openstudiomodel.AirGap(model, thermal_resistance)

        if name is not None: gap.setName(name)
        return gap

    @staticmethod
    def glazing_material(
            model: openstudio.openstudiomodel.Model,
            name=None,
            optical_data_type: str = "SpectralAverage",
            thickness=0.003,
            solar_transmittance_normal=0.8,
            front_solar_reflectance=0.08,
            back_solar_reflectance=0.08,
            visible_transmittance_normal=0.9,
            front_visible_reflectance=0.08,
            back_visible_reflectance=0.0,
            infrared_transmittance_normal=0.0,
            front_infrared_hemi_emissivity=0.8,
            back_infrared_hemi_emissivity=0.8,
            conductivity=0.9,
            solar_diffusing=False):
        glazing = openstudio.openstudiomodel.StandardGlazing(model)
        if name is not None:
            glazing.setName(name)
        glazing.setOpticalDataType(optical_data_type)
        glazing.setThickness(thickness)
        glazing.setSolarTransmittance(solar_transmittance_normal)
        glazing.setFrontSideSolarReflectanceatNormalIncidence(front_solar_reflectance)
        glazing.setBackSideSolarReflectanceatNormalIncidence(back_solar_reflectance)
        glazing.setVisibleTransmittance(visible_transmittance_normal)
        glazing.setFrontSideVisibleReflectanceatNormalIncidence(front_visible_reflectance)
        glazing.setBackSideVisibleReflectanceatNormalIncidence(back_visible_reflectance)
        glazing.setInfraredTransmittance(infrared_transmittance_normal)
        glazing.setFrontSideInfraredHemisphericalEmissivity(front_infrared_hemi_emissivity)
        glazing.setBackSideInfraredHemisphericalEmissivity(back_infrared_hemi_emissivity)
        glazing.setConductivity(conductivity)
        glazing.setSolarDiffusing(solar_diffusing)

        return glazing

    @staticmethod
    def gas_window_material(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            gas_type: str = "Air",
            thickness=0.01,
            conductivity_coeff_a=None,
            conductivity_coeff_b=None,
            conductivity_coeff_c=None,
            viscosity_coeff_a=None,
            viscosity_coeff_b=None,
            viscosity_coeff_c=None,
            specific_heat_coeff_a=None,
            specific_heat_coeff_b=None,
            specific_heat_coeff_c=None,
            specific_heat_ratio=None,
            molecular_weight=None):
        gas = openstudio.openstudiomodel.Gas(model)
        if name is not None: gas.setName(name)
        if gas_type is not None:
            gas.setGasType(gas_type)
        if thickness is not None:
            gas.setThickness(thickness)
        if conductivity_coeff_a is not None:
            gas.setConductivityCoefficientA(conductivity_coeff_a)
        if conductivity_coeff_b is not None:
            gas.setConductivityCoefficientB(conductivity_coeff_b)
        if conductivity_coeff_c is not None:
            gas.setConductivityCoefficientC(conductivity_coeff_c)
        if viscosity_coeff_a is not None:
            gas.setViscosityCoefficientA(viscosity_coeff_a)
        if viscosity_coeff_b is not None:
            gas.setViscosityCoefficientB(viscosity_coeff_b)
        if viscosity_coeff_c is not None:
            gas.setViscosityCoefficientC(viscosity_coeff_c)
        if specific_heat_coeff_a is not None:
            gas.setSpecificHeatCoefficientA(specific_heat_coeff_a)
        if specific_heat_coeff_b is not None:
            gas.setSpecificHeatCoefficientB(specific_heat_coeff_b)
        if specific_heat_coeff_c is not None:
            gas.setSpecificHeatCoefficientC(specific_heat_coeff_c)
        if specific_heat_ratio is not None:
            gas.setSpecificHeatRatio(specific_heat_ratio)
        if molecular_weight is not None:
            gas.setMolecularWeight(molecular_weight)


