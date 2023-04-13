from openstudio.openstudiomodel import Lights, ElectricEquipment, People
from openstudio.openstudiomodel import GasEquipment, InternalMass, WaterUseEquipment
from openstudio.openstudiomodel import LightsDefinition, ElectricEquipmentDefinition, PeopleDefinition
from openstudio.openstudiomodel import GasEquipmentDefinition, InternalMassDefinition, WaterUseEquipmentDefinition
from openstudio.openstudiomodel import DesignSpecificationOutdoorAir, SpaceInfiltrationDesignFlowRate
from Schedules.ScheduleTools import ScheduleTool
import json


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
        if schedule is not None:
            infiltration.setSchedule(schedule)

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

    @staticmethod
    def water_use_equipment(
            model,
            peak_flow_rate=0.000525,
            target_temp=135,
            space=None,
            flow_rate_fraction_schedule=None):

        water_use_def = WaterUseEquipmentDefinition(model)
        water_use_def.setPeakFlowRate(peak_flow_rate)

        # Schedules:
        temp_type_limit = ScheduleTool.schedule_type_limits(model, 2, 1, 0, 100)
        temp_schedule = ScheduleTool.schedule_ruleset(model, target_temp, temp_type_limit)

        ratio_type_limit = ScheduleTool.schedule_type_limits(model, 1, 1, 0, 1)
        sensible_schedule = ScheduleTool.schedule_ruleset(model, 0.2, ratio_type_limit)
        latent_schedule = ScheduleTool.schedule_ruleset(model, 0.05, ratio_type_limit)

        water_use_def.setTargetTemperatureSchedule(temp_schedule)
        water_use_def.setSensibleFractionSchedule(sensible_schedule)
        water_use_def.setLatentFractionSchedule(latent_schedule)

        water_use = WaterUseEquipment(water_use_def)

        if flow_rate_fraction_schedule is not None:
            water_use.setFlowRateFractionSchedule(flow_rate_fraction_schedule)
        else:
            water_use.setFlowRateFractionSchedule(ScheduleTool.dhw_flow_fraction_schedule(model))

        if space is not None:
            water_use.setSpace(space)

        return water_use

    @staticmethod
    def internal_load_input_json(
            space_type=None,
            lighting=None,
            equipment=None,
            people_density=None,
            people_activity_level=None,
            outdoor_air_per_area=None,
            outdoor_air_per_person=None):

        internal_load = {}

        if space_type is not None and isinstance(space_type, list):
            for i, space in enumerate(space_type):
                load_dict = {}
                if lighting is not None and isinstance(lighting, list):
                    try:
                        load_dict["lighting"] = lighting[i]
                    except IndexError:
                        load_dict["lighting"] = lighting[-1]
                        print("Cannot find lighting value for space {}".format(space))
                else:
                    load_dict["lighting"] = None

                if equipment is not None and isinstance(equipment, list):
                    try:
                        load_dict["equipment"] = equipment[i]
                    except IndexError:
                        load_dict["equipment"] = equipment[-1]
                else:
                    load_dict["equipment"] = None

                if people_density is not None and isinstance(people_density, list):
                    try:
                        load_dict["people_density"] = people_density[i]
                    except IndexError:
                        load_dict["people_density"] = people_density[-1]
                else:
                    load_dict["people_density"] = None

                if people_activity_level is not None and isinstance(people_activity_level, list):
                    try:
                        load_dict["people_activity_level"] = people_activity_level[i]
                    except IndexError:
                        load_dict["people_activity_level"] = people_activity_level[-1]
                else:
                    load_dict["people_activity_level"] = None

                if outdoor_air_per_area is not None and isinstance(outdoor_air_per_area, list):
                    try:
                        load_dict["outdoor_air_per_area"] = outdoor_air_per_area[i]
                    except IndexError:
                        load_dict["outdoor_air_per_area"] = outdoor_air_per_area[-1]
                else:
                    load_dict["outdoor_air_per_area"] = None

                if outdoor_air_per_person is not None and isinstance(outdoor_air_per_person, list):
                    try:
                        load_dict["outdoor_air_per_person"] = outdoor_air_per_person[i]
                    except IndexError:
                        load_dict["outdoor_air_per_person"] = outdoor_air_per_person[-1]
                else:
                    load_dict["outdoor_air_per_person"] = None

                internal_load[space] = load_dict

        internal_load_json = json.dumps(internal_load, indent=4)

        return internal_load_json



