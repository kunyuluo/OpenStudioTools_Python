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
            roughness: int = 1,
            thermal_absorptance=None,
            solar_absorptance=None,
            visible_absorptance=None):

        """
        Roughness: 1.VeryRough 2.Rough 3.MediumRough 4.MediumSmooth 5.Smooth 6.VerySmooth
        """

        roughness_options = {1: "VeryRough", 2: "Rough", 3: "MediumRough", 4: "MediumSmooth", 5: "Smooth", 6: "VerySmooth"}

        mat = StandardOpaqueMaterial(model)
        mat.setName(name)

        if thickness is not None:
            mat.setThickness(thickness)
        if conductivity is not None:
            mat.setConductivity(conductivity)
        if density is not None:
            mat.setDensity(density)
        if specific_heat is not None:
            mat.setSpecificHeat(specific_heat)
        if roughness is not None:
            mat.setRoughness(roughness_options[roughness])
        if thermal_absorptance is not None:
            mat.setThermalAbsorptance(thermal_absorptance)
        if solar_absorptance is not None:
            mat.setSolarAbsorptance(solar_absorptance)
        if visible_absorptance is not None:
            mat.setVisibleAbsorptance(visible_absorptance)

        return mat

    @staticmethod
    def construction(model: openstudio.openstudiomodel.Model, name=None):
        cons = openstudio.openstudiomodel.Construction(model)

        if name is not None:
            cons.setName(name)

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
    def opaque_cons(
            model: openstudio.openstudiomodel.Model,
            name,
            thickness=None,
            conductivity=None,
            density=None,
            specific_heat=None,
            roughness: int = 1,
            thermal_absorptance=None,
            solar_absorptance=None,
            visible_absorptance=None):

        """
        Roughness: 1.VeryRough 2.Rough 3.MediumRough 4.MediumSmooth 5.Smooth 6.VerySmooth
        """

        mat = ConstructionTool.opaque_standard_material(
            model, name, thickness, conductivity, density, specific_heat, roughness,
            thermal_absorptance, solar_absorptance, visible_absorptance)

        mat_vec = MaterialVector()
        mat_vec.append(mat)

        cons = Construction(model)
        cons.setName(name)
        cons.setLayers(mat_vec)

        return cons

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

    @staticmethod
    def construction_set(
            model: openstudio.openstudiomodel.Model,
            exterior_wall: openstudio.openstudiomodel.Construction = None,
            exterior_roof: openstudio.openstudiomodel.Construction = None,
            exterior_floor: openstudio.openstudiomodel.Construction = None,
            exterior_fixed_window: openstudio.openstudiomodel.Construction = None,
            exterior_operable_window: openstudio.openstudiomodel.Construction = None,
            interior_wall: openstudio.openstudiomodel.Construction = None,
            interior_roof: openstudio.openstudiomodel.Construction = None,
            interior_floor: openstudio.openstudiomodel.Construction = None,
            underground_wall: openstudio.openstudiomodel.Construction = None,
            underground_roof: openstudio.openstudiomodel.Construction = None,
            underground_floor: openstudio.openstudiomodel.Construction = None,
            name: str = None):

        sets = openstudio.openstudiomodel.DefaultConstructionSet(model)

        if name is not None:
            sets.setName(name)

        # Exterior Surfaces:
        # *******************************************************************************************************
        exterior_surfaces = openstudio.openstudiomodel.DefaultSurfaceConstructions(model)

        if exterior_wall is not None:
            exterior_surfaces.setWallConstruction(exterior_wall)

        if exterior_roof is not None:
            exterior_surfaces.setRoofCeilingConstruction(exterior_roof)

        if exterior_floor is not None:
            exterior_surfaces.setFloorConstruction(exterior_floor)

        sets.setDefaultExteriorSurfaceConstructions(exterior_surfaces)

        # Interior Surfaces:
        # *******************************************************************************************************
        interior_surfaces = openstudio.openstudiomodel.DefaultSurfaceConstructions(model)

        if interior_wall is not None:
            interior_surfaces.setWallConstruction(interior_wall)

        if interior_roof is not None:
            interior_surfaces.setRoofCeilingConstruction(interior_roof)

        if interior_floor is not None:
            interior_surfaces.setFloorConstruction(interior_floor)

        sets.setDefaultInteriorSurfaceConstructions(interior_surfaces)

        # Exterior SubSurfaces:
        # *******************************************************************************************************
        exterior_subsurfaces = openstudio.openstudiomodel.DefaultSubSurfaceConstructions(model)

        if exterior_fixed_window is not None:
            exterior_subsurfaces.setFixedWindowConstruction(exterior_fixed_window)

        if exterior_operable_window is not None:
            exterior_subsurfaces.setOperableWindowConstruction(exterior_operable_window)

        sets.setDefaultExteriorSubSurfaceConstructions(exterior_subsurfaces)

        # Underground Surfaces:
        # *******************************************************************************************************
        underground_surfaces = openstudio.openstudiomodel.DefaultSurfaceConstructions(model)

        if underground_wall is not None:
            underground_surfaces.setWallConstruction(underground_wall)

        if interior_roof is not None:
            underground_surfaces.setRoofCeilingConstruction(underground_roof)

        if interior_floor is not None:
            underground_surfaces.setFloorConstruction(underground_floor)

        sets.setDefaultInteriorSurfaceConstructions(underground_surfaces)

        return sets

    @staticmethod
    def construction_set_simple(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            unit_r_or_u: bool = True,
            ext_wall_r_value=10,
            ext_roof_r_value=10,
            ext_floor_r_value=10,
            win_u_value=2.0,
            win_shgc=0.5,
            win_transmittance=0.5,
            int_wall_r_value=10,
            int_floor_r_value=10,
            ground_wall_r_value=10,
            ground_roof_r_value=10,
            ground_floor_r_value=10):

        """
        Unit_r_or_u:
        set to True if all input values below are R-value (thermal resistance).
        Otherwise, they will be U-value (conductivity).
        """

        sets = openstudio.openstudiomodel.DefaultConstructionSet(model)

        if name is not None:
            sets.setName(name)

        # Exterior Surfaces:
        # *******************************************************************************************************
        exterior_surfaces = openstudio.openstudiomodel.DefaultSurfaceConstructions(model)

        # Wall:
        # ***************************************************************************************
        if unit_r_or_u:
            exterior_wall_cons = ConstructionTool.opaque_no_mass_cons(
                model, "R-{} ExtWall".format(round(ext_wall_r_value, 1)), ext_wall_r_value)
        else:
            exterior_wall_cons = ConstructionTool.opaque_no_mass_cons(
                model, "R-{} ExtWall".format(round(1 / ext_wall_r_value, 1)), 1 / ext_wall_r_value)
        exterior_surfaces.setWallConstruction(exterior_wall_cons)

        # Roof:
        # ***************************************************************************************
        if unit_r_or_u:
            exterior_roof_cons = ConstructionTool.opaque_no_mass_cons(
                model, "R-{} ExtRoof".format(round(ext_roof_r_value, 1)), ext_roof_r_value)
        else:
            exterior_roof_cons = ConstructionTool.opaque_no_mass_cons(
                model, "R-{} ExtRoof".format(round(1 / ext_roof_r_value, 1)), 1 / ext_roof_r_value)
        exterior_surfaces.setRoofCeilingConstruction(exterior_roof_cons)

        # Floor:
        # ***************************************************************************************
        if unit_r_or_u:
            exterior_floor_cons = ConstructionTool.opaque_no_mass_cons(
                model, "R-{} ExtFloor".format(round(ext_floor_r_value, 1)), ext_floor_r_value)
        else:
            exterior_floor_cons = ConstructionTool.opaque_no_mass_cons(
                model, "R-{} ExtFloor".format(round(1 / ext_floor_r_value, 1)), 1 / ext_floor_r_value)
        exterior_surfaces.setFloorConstruction(exterior_floor_cons)

        sets.setDefaultExteriorSurfaceConstructions(exterior_surfaces)

        # Interior Surfaces:
        # *******************************************************************************************************
        interior_surfaces = openstudio.openstudiomodel.DefaultSurfaceConstructions(model)
        # Wall:
        # ***************************************************************************************
        if unit_r_or_u:
            interior_wall_cons = ConstructionTool.opaque_no_mass_cons(
                model, "R-{} IntWall".format(round(int_wall_r_value, 1)), int_wall_r_value)
        else:
            interior_wall_cons = ConstructionTool.opaque_no_mass_cons(
                model, "R-{} IntWall".format(round(1 / int_wall_r_value, 1)), 1 / int_wall_r_value)
        interior_surfaces.setWallConstruction(interior_wall_cons)

        # Floor:
        # ***************************************************************************************
        if unit_r_or_u:
            interior_floor_cons = ConstructionTool.opaque_no_mass_cons(
                model, "R-{} IntFloor".format(round(int_floor_r_value, 1)), int_floor_r_value)
        else:
            interior_floor_cons = ConstructionTool.opaque_no_mass_cons(
                model, "R-{} IntFloor".format(round(1 / int_floor_r_value, 1)), 1 / int_floor_r_value)
        interior_surfaces.setFloorConstruction(interior_floor_cons)

        # Ceiling:
        # ***************************************************************************************
        interior_surfaces.setRoofCeilingConstruction(interior_floor_cons)

        sets.setDefaultInteriorSurfaceConstructions(interior_surfaces)

        # Exterior SubSurfaces:
        # *******************************************************************************************************
        exterior_subsurfaces = openstudio.openstudiomodel.DefaultSubSurfaceConstructions(model)
        # Fixed window:
        # ***************************************************************************************
        exterior_fixed_window_cons = ConstructionTool.simple_glazing_cons(
            model, "Fixed_Window", win_u_value, win_shgc, win_transmittance)
        exterior_subsurfaces.setFixedWindowConstruction(exterior_fixed_window_cons)

        # Operable window:
        # ***************************************************************************************
        exterior_operable_window_cons = ConstructionTool.simple_glazing_cons(
            model, "Operable_Window", win_u_value, win_shgc, win_transmittance)
        exterior_subsurfaces.setOperableWindowConstruction(exterior_operable_window_cons)

        sets.setDefaultExteriorSubSurfaceConstructions(exterior_subsurfaces)

        # Ground Surfaces:
        # *******************************************************************************************************
        ground_surfaces = openstudio.openstudiomodel.DefaultSurfaceConstructions(model)
        # Wall:
        # ***************************************************************************************
        if unit_r_or_u:
            ground_wall_cons = ConstructionTool.opaque_no_mass_cons(
                model, "R-{} Underground_Wall".format(round(ground_wall_r_value, 1)), ground_wall_r_value)
        else:
            ground_wall_cons = ConstructionTool.opaque_no_mass_cons(
                model, "R-{} Underground_Wall".format(round(1 / ground_wall_r_value, 1)), 1 / ground_wall_r_value)
        ground_surfaces.setWallConstruction(ground_wall_cons)

        # Ceiling:
        # ***************************************************************************************
        if unit_r_or_u:
            ground_roof_cons = ConstructionTool.opaque_no_mass_cons(
                model, "R-{} Underground_Roof".format(round(ground_roof_r_value, 1)), ground_roof_r_value)
        else:
            ground_roof_cons = ConstructionTool.opaque_no_mass_cons(
                model, "R-{} Underground_Roof".format(round(1 / ground_roof_r_value, 1)), 1 / ground_roof_r_value)
        ground_surfaces.setRoofCeilingConstruction(ground_roof_cons)

        # Floor:
        # ***************************************************************************************
        if unit_r_or_u:
            ground_floor_cons = ConstructionTool.opaque_no_mass_cons(
                model, "R-{} Underground_Floor".format(round(ground_floor_r_value, 1)), ground_floor_r_value)
        else:
            ground_floor_cons = ConstructionTool.opaque_no_mass_cons(
                model, "R-{} Underground_Floor".format(round(1 / ground_floor_r_value, 1)), 1 / ground_floor_r_value)
        ground_surfaces.setFloorConstruction(ground_floor_cons)

        sets.setDefaultGroundContactSurfaceConstructions(ground_surfaces)

        # Output:
        # *******************************************************************************************************
        return sets
