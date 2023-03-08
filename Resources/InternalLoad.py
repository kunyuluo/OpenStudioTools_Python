from openstudio.openstudiomodel import Lights, ElectricEquipment, People
from openstudio.openstudiomodel import GasEquipment, InternalMass
from openstudio.openstudiomodel import LightsDefinition, ElectricEquipmentDefinition, PeopleDefinition
from openstudio.openstudiomodel import GasEquipmentDefinition, InternalMassDefinition
from openstudio.openstudiomodel import DesignSpecificationOutdoorAir, SpaceInfiltrationDesignFlowRate


class InternalLoad:

    @staticmethod
    def add_gas_equipment(model, space, gas_power=0, schedule=None):
        gas_def = GasEquipmentDefinition(model)
        gas_def.setWattsperSpaceFloorArea(gas_power)
        gas = GasEquipment(gas_def)
        if schedule is not None: gas.setSchedule(schedule)
        gas.setSpace(space)

    @staticmethod
    def add_internal_mass(model, space=None, area_calc_method="SurfaceArea", surface_area=0, construction=None):
        mass_def = InternalMassDefinition(model)

        if area_calc_method == "SurfaceArea":
            mass_def.setSurfaceArea(surface_area)
        elif area_calc_method == "SurfaceArea/Area":
            mass_def.setSurfaceAreaperSpaceFloorArea(surface_area)
        elif area_calc_method == "SurfaceArea/Person":
            mass_def.setSurfaceAreaperPerson(surface_area)
        else:
            mass_def.setSurfaceArea(surface_area)

        if construction is not None: mass_def.setConstruction(construction)

        mass = InternalMass(mass_def)
        if space is not None: mass.setSpace(space)

    @staticmethod
    def add_lights(model, space, power_calc_method: str = "Watts/Area", lighting_power=0, lighting_schedule=None):
        lighting_def = LightsDefinition(model)

        if power_calc_method == "LightingLevel":
            lighting_def.setLightingLevel(lighting_power)
        elif power_calc_method == "Watts/Area":
            lighting_def.setWattsperSpaceFloorArea(lighting_power)
        elif power_calc_method == "Watts/Person":
            lighting_def.setWattsperPerson(lighting_power)
        else:
            lighting_def.setLightingLevel(lighting_power)

        light = Lights(lighting_def)
        if lighting_schedule is not None: light.setSchedule(lighting_schedule)
        light.setSpace(space)

    @staticmethod
    def add_electric_equipment(model, space, power_calc_method: str = "Watts/Area", power=0, schedule=None):
        equip_def = ElectricEquipmentDefinition(model)

        if power_calc_method == "EquipmentLevel":
            equip_def.setDesignLevel(power)
        elif power_calc_method == "Watts/Area":
            equip_def.setWattsperSpaceFloorArea(power)
        elif power_calc_method == "Watts/Person":
            equip_def.setWattsperPerson(power)
        else:
            equip_def.setDesignLevel(power)

        equip = ElectricEquipment(equip_def)
        if schedule is not None: equip.setSchedule(schedule)
        equip.setSpace(space)

    @staticmethod
    def add_people(model,
               space,
               ppl_calc_method: str = "People/Area",
               amount=0,
               schedule=None,
               activity_schedule=None,
               fraction_radiant=None,
               sensible_heat_fraction=None,
               co2_generation_rate=None,
               enable_ashrae55_warning=False,
               mrt_calc_type="ZoneAveraged",  # Options: ZoneAveraged, SurfaceWeighted, AngleFactor
               thermal_comfort_model_type=None):

        ppl_def = PeopleDefinition(model)

        if ppl_calc_method == "People":
            ppl_def.setNumberofPeople(amount)
        elif ppl_calc_method == "People/Area":
            ppl_def.setPeopleperSpaceFloorArea(amount)
        elif ppl_calc_method == "Area/Person":
            ppl_def.setSpaceFloorAreaperPerson(amount)
        else:
            ppl_def.setNumberofPeople(amount)

        if fraction_radiant is not None:
            ppl_def.setFractionRadiant(fraction_radiant)
        if sensible_heat_fraction is not None:
            ppl_def.setSensibleHeatFraction(sensible_heat_fraction)
        if co2_generation_rate is not None:
            ppl_def.setCarbonDioxideGenerationRate(co2_generation_rate)
        if enable_ashrae55_warning:
            ppl_def.setEnableASHRAE55ComfortWarnings(True)
        if mrt_calc_type is not None:
            ppl_def.setMeanRadiantTemperatureCalculationType(mrt_calc_type)

        # Alternatives of thermal comfort model type:
        # *******************************************************************
        # Fanger
        # Pierce
        # KSU
        # AdaptiveASH55
        # AdaptiveCEN15251
        # CoolingEffectASH55
        # AnkleDraftASH55
        # *******************************************************************
        if thermal_comfort_model_type is not None and len(thermal_comfort_model_type) != 0:
            for i in range(len(thermal_comfort_model_type)):
                ppl_def.pushThermalComfortModelType(thermal_comfort_model_type[i])

        ppl = People(ppl_def)
        if schedule is not None: ppl.setNumberofPeopleSchedule(schedule)
        if activity_schedule is not None: ppl.setActivityLevelSchedule(activity_schedule)
        ppl.setSpace(space)

    @staticmethod
    def add_infiltration(model, space_type, schedule=None):
        infiltration = SpaceInfiltrationDesignFlowRate(model)
        infiltration.setSpaceType(space_type)
        infiltration.setFlowperExteriorSurfaceArea(0.000226568446)
        if schedule is not None: infiltration.setSchedule(schedule)

    @staticmethod
    def add_outdoor_air(model, space_type, outdoor_air_per_floor_area=0, outdoor_air_per_person=0,
                    schedule=None):

        outdoor_air = DesignSpecificationOutdoorAir(model)
        outdoor_air.setName(space_type.nameString() + "_DSOA")
        outdoor_air.setOutdoorAirMethod("Sum")
        outdoor_air.setOutdoorAirFlowperFloorArea(outdoor_air_per_floor_area)
        outdoor_air.setOutdoorAirFlowperPerson(outdoor_air_per_person)
        if schedule is not None: outdoor_air.setOutdoorAirFlowRateFractionSchedule(schedule)

        space_type.setDesignSpecificationOutdoorAir(outdoor_air)
