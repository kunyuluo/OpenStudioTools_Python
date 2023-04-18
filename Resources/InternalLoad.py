from openstudio.openstudiomodel import Lights, ElectricEquipment, People
from openstudio.openstudiomodel import GasEquipment, InternalMass, WaterUseEquipment
from openstudio.openstudiomodel import LightsDefinition, ElectricEquipmentDefinition, PeopleDefinition
from openstudio.openstudiomodel import GasEquipmentDefinition, InternalMassDefinition, WaterUseEquipmentDefinition
from openstudio.openstudiomodel import DesignSpecificationOutdoorAir, SpaceInfiltrationDesignFlowRate
from Schedules.ScheduleTools import ScheduleTool
import openstudio
import json


class InternalLoad:

    @staticmethod
    def gas_equipment_definition(
            model: openstudio.openstudiomodel.Model,
            gas_power: float = 0):

        gas_def = GasEquipmentDefinition(model)
        gas_def.setWattsperSpaceFloorArea(gas_power)

        return gas_def

    @staticmethod
    def gas_equipment(
            gas_definition: GasEquipmentDefinition,
            space: openstudio.openstudiomodel.Space = None,
            schedule: openstudio.openstudiomodel.ScheduleRuleset = None):

        gas = GasEquipment(gas_definition)
        if schedule is not None:
            gas.setSchedule(schedule)

        if space is not None:
            gas.setSpace(space)

        return gas

    @staticmethod
    def add_gas_equipment(
            model: openstudio.openstudiomodel.Model,
            space: openstudio.openstudiomodel.Space = None,
            gas_power: float = 0,
            schedule: openstudio.openstudiomodel.ScheduleRuleset = None):

        gas_def = GasEquipmentDefinition(model)
        gas_def.setWattsperSpaceFloorArea(gas_power)

        gas = GasEquipment(gas_def)
        if schedule is not None:
            gas.setSchedule(schedule)

        if space is not None:
            gas.setSpace(space)

        return gas

    @staticmethod
    def internal_mass_definition(
            model: openstudio.openstudiomodel.Model,
            area_calc_method: int = 1,
            surface_area: float = None,
            construction=None):

        """
        Area_calc_method: \n
        1.SurfaceArea 2.SurfaceArea/Area 3.SurfaceArea/Person
        """

        mass_def = InternalMassDefinition(model)

        match area_calc_method:
            case 1:
                try:
                    mass_def.setSurfaceArea(surface_area)
                except ValueError:
                    print("Invalid input of surface area.")
            case 2:
                try:
                    mass_def.setSurfaceAreaperSpaceFloorArea(surface_area)
                except ValueError:
                    print("Invalid input of surface area.")
            case 3 | _:
                try:
                    mass_def.setSurfaceAreaperPerson(surface_area)
                except ValueError:
                    print("Invalid input of surface area.")

        if construction is not None:
            mass_def.setConstruction(construction)

        return mass_def

    @staticmethod
    def internal_mass(
            mass_definition: InternalMassDefinition,
            space: openstudio.openstudiomodel.Space = None):

        mass = InternalMass(mass_definition)

        if space is not None:
            mass.setSpace(space)

        return mass

    @staticmethod
    def add_internal_mass(
            model: openstudio.openstudiomodel.Model,
            space: openstudio.openstudiomodel.Space = None,
            area_calc_method: int = 1,
            surface_area: float = 0.0,
            construction=None):

        """
        Area_calc_method: \n
        1.SurfaceArea 2.SurfaceArea/Area 3.SurfaceArea/Person
        """

        mass_def = InternalMassDefinition(model)

        match area_calc_method:
            case 1:
                mass_def.setSurfaceArea(surface_area)
            case 2:
                mass_def.setSurfaceAreaperSpaceFloorArea(surface_area)
            case 3 | _:
                mass_def.setSurfaceAreaperPerson(surface_area)

        if construction is not None:
            mass_def.setConstruction(construction)

        mass = InternalMass(mass_def)

        if space is not None:
            mass.setSpace(space)

        return mass

    @staticmethod
    def light_definition(
            model: openstudio.openstudiomodel.Model,
            power_calc_method: int = 3,
            lighting_power: float = 0):

        """
        -Power_calc_method: \n
        1.LightingLevel 2.Watts/Person 3.Watts/Area \n
        (Default is 3)
        """

        lighting_def = LightsDefinition(model)

        match power_calc_method:
            case 1:
                lighting_def.setLightingLevel(lighting_power)
            case 2:
                lighting_def.setWattsperPerson(lighting_power)
            case 3 | _:
                lighting_def.setWattsperSpaceFloorArea(lighting_power)

        return lighting_def

    @staticmethod
    def light(
            light_definition: LightsDefinition,
            space: openstudio.openstudiomodel.Space = None,
            lighting_schedule: openstudio.openstudiomodel.ScheduleRuleset = None):

        light = Lights(light_definition)

        if lighting_schedule is not None:
            light.setSchedule(lighting_schedule)

        if space is not None:
            light.setSpace(space)

        return light

    @staticmethod
    def add_lights(
            model: openstudio.openstudiomodel.Model,
            space: openstudio.openstudiomodel.Space = None,
            power_calc_method: int = 3,
            lighting_power: float = 0,
            lighting_schedule: openstudio.openstudiomodel.ScheduleRuleset = None):

        """
        -Power_calc_method: \n
        1.LightingLevel 2.Watts/Person 3.Watts/Area \n
        (Default is 3)
        """

        lighting_def = LightsDefinition(model)

        match power_calc_method:
            case 1:
                lighting_def.setLightingLevel(lighting_power)
            case 2:
                lighting_def.setWattsperPerson(lighting_power)
            case 3 | _:
                lighting_def.setWattsperSpaceFloorArea(lighting_power)

        light = Lights(lighting_def)

        if lighting_schedule is not None:
            light.setSchedule(lighting_schedule)

        if space is not None:
            light.setSpace(space)

        return light

    @staticmethod
    def electric_equipment_definition(
            model: openstudio.openstudiomodel.Model,
            power_calc_method: int = 3,
            power: float = 0):

        """
        -Power_calc_method: \n
        1.EquipmentLevel 2.Watts/Person 3.Watts/Area \n
        (Default is 3)
        """

        equip_def = ElectricEquipmentDefinition(model)

        match power_calc_method:
            case 1:
                equip_def.setDesignLevel(power)
            case 2:
                equip_def.setWattsperPerson(power)
            case 3 | _:
                equip_def.setWattsperSpaceFloorArea(power)

        return equip_def

    @staticmethod
    def electric_equipment(
            equip_definition: ElectricEquipmentDefinition,
            space: openstudio.openstudiomodel.Space = None,
            schedule: openstudio.openstudiomodel.ScheduleRuleset = None):

        equip = ElectricEquipment(equip_definition)

        if schedule is not None:
            equip.setSchedule(schedule)

        if space is not None:
            equip.setSpace(space)

        return equip

    @staticmethod
    def add_electric_equipment(
            model: openstudio.openstudiomodel.Model,
            space: openstudio.openstudiomodel.Space = None,
            power_calc_method: int = 3,
            power: float = 0,
            schedule: openstudio.openstudiomodel.ScheduleRuleset = None):

        """
        -Power_calc_method: \n
        1.EquipmentLevel 2.Watts/Person 3.Watts/Area \n
        (Default is 3)
        """

        equip_def = ElectricEquipmentDefinition(model)

        match power_calc_method:
            case 1:
                equip_def.setDesignLevel(power)
            case 2:
                equip_def.setWattsperPerson(power)
            case 3 | _:
                equip_def.setWattsperSpaceFloorArea(power)

        equip = ElectricEquipment(equip_def)

        if schedule is not None:
            equip.setSchedule(schedule)

        if space is not None:
            equip.setSpace(space)

        return equip

    @staticmethod
    def add_people(
            model: openstudio.openstudiomodel.Model,
            space: openstudio.openstudiomodel.Space = None,
            ppl_calc_method: int = 2,
            amount: int = 0,
            schedule: openstudio.openstudiomodel.ScheduleRuleset = None,
            activity_schedule: openstudio.openstudiomodel.ScheduleRuleset = None,
            fraction_radiant=None,
            sensible_heat_fraction=None,
            co2_generation_rate=None,
            enable_ashrae55_warning=False,
            mrt_calc_type: int = 1,
            thermal_comfort_model_type=None):

        """
        -ppl_calc_method: \n
        1.People 2.Area/Person 3.People/Area \n

        -mrt_calc_type: \n
        1.ZoneAveraged 2.SurfaceWeighted 3.AngleFactor \n

        -Thermal comfort model type: \n
        1.Fanger 2.Pierce 3.KSU 4.AdaptiveASH55 5.AdaptiveCEN15251 6.AdaptiveCEN15251 7.AnkleDraftASH55
        """

        mrt_methods = {1: "ZoneAveraged", 2: "SurfaceWeighted", 3: "AngleFactor"}
        thermal_comfort_types = {1: "Fanger", 2: "Pierce", 3: "KSU", 4: "AdaptiveASH55",
                                 5: "AdaptiveCEN15251", 6: "AdaptiveCEN15251", 7: "AnkleDraftASH55"}

        ppl_def = PeopleDefinition(model)

        match ppl_calc_method:
            case 1:
                ppl_def.setNumberofPeople(amount)
            case 2:
                ppl_def.setSpaceFloorAreaperPerson(amount)
            case 3 | _:
                ppl_def.setPeopleperSpaceFloorArea(amount)

        if fraction_radiant is not None:
            ppl_def.setFractionRadiant(fraction_radiant)
        if sensible_heat_fraction is not None:
            ppl_def.setSensibleHeatFraction(sensible_heat_fraction)
        if co2_generation_rate is not None:
            ppl_def.setCarbonDioxideGenerationRate(co2_generation_rate)
        if enable_ashrae55_warning:
            ppl_def.setEnableASHRAE55ComfortWarnings(True)
        if mrt_calc_type is not None:
            ppl_def.setMeanRadiantTemperatureCalculationType(mrt_methods[mrt_calc_type])

        if thermal_comfort_model_type is not None:
            if isinstance(thermal_comfort_model_type, int):
                ppl_def.pushThermalComfortModelType(thermal_comfort_types[thermal_comfort_model_type])
            elif isinstance(thermal_comfort_model_type, list):
                for i in thermal_comfort_model_type:
                    ppl_def.pushThermalComfortModelType(thermal_comfort_types[i])
            else:
                raise TypeError("Invalid input type of thermal_comfort_model_type."
                                "It must be a single integer or a list of integer")

        ppl = People(ppl_def)

        if schedule is not None:
            ppl.setNumberofPeopleSchedule(schedule)

        if activity_schedule is not None:
            ppl.setActivityLevelSchedule(activity_schedule)

        if space is not None:
            ppl.setSpace(space)

        return ppl

    @staticmethod
    def people_definition(
            model: openstudio.openstudiomodel.Model,
            ppl_calc_method: int = 2,
            amount: int = 0,
            fraction_radiant=None,
            sensible_heat_fraction=None,
            co2_generation_rate=None,
            enable_ashrae55_warning=False,
            mrt_calc_type: int = 1,
            thermal_comfort_model_type=None):

        """
        -ppl_calc_method: \n
        1.People 2.Area/Person 3.People/Area \n

        -mrt_calc_type: \n
        1.ZoneAveraged 2.SurfaceWeighted 3.AngleFactor \n

        -Thermal comfort model type: \n
        1.Fanger 2.Pierce 3.KSU 4.AdaptiveASH55 5.AdaptiveCEN15251 6.AdaptiveCEN15251 7.AnkleDraftASH55
        """

        mrt_methods = {1: "ZoneAveraged", 2: "SurfaceWeighted", 3: "AngleFactor"}
        thermal_comfort_types = {1: "Fanger", 2: "Pierce", 3: "KSU", 4: "AdaptiveASH55",
                                 5: "AdaptiveCEN15251", 6: "AdaptiveCEN15251", 7: "AnkleDraftASH55"}

        ppl_def = PeopleDefinition(model)

        match ppl_calc_method:
            case 1:
                ppl_def.setNumberofPeople(amount)
            case 2:
                ppl_def.setSpaceFloorAreaperPerson(amount)
            case 3 | _:
                ppl_def.setPeopleperSpaceFloorArea(amount)

        if fraction_radiant is not None:
            ppl_def.setFractionRadiant(fraction_radiant)
        if sensible_heat_fraction is not None:
            ppl_def.setSensibleHeatFraction(sensible_heat_fraction)
        if co2_generation_rate is not None:
            ppl_def.setCarbonDioxideGenerationRate(co2_generation_rate)
        if enable_ashrae55_warning:
            ppl_def.setEnableASHRAE55ComfortWarnings(True)
        if mrt_calc_type is not None:
            ppl_def.setMeanRadiantTemperatureCalculationType(mrt_methods[mrt_calc_type])

        if thermal_comfort_model_type is not None:
            if isinstance(thermal_comfort_model_type, int):
                ppl_def.pushThermalComfortModelType(thermal_comfort_types[thermal_comfort_model_type])
            elif isinstance(thermal_comfort_model_type, list):
                for i in thermal_comfort_model_type:
                    ppl_def.pushThermalComfortModelType(thermal_comfort_types[i])
            else:
                raise TypeError("Invalid input type of thermal_comfort_model_type."
                                "It must be a single integer or a list of integer")

        return ppl_def

    @staticmethod
    def people(
            people_definition: PeopleDefinition,
            space: openstudio.openstudiomodel.Space = None,
            schedule: openstudio.openstudiomodel.ScheduleRuleset = None,
            activity_schedule: openstudio.openstudiomodel.ScheduleRuleset = None):

        ppl = People(people_definition)

        if schedule is not None:
            ppl.setNumberofPeopleSchedule(schedule)

        if activity_schedule is not None:
            ppl.setActivityLevelSchedule(activity_schedule)

        if space is not None:
            ppl.setSpace(space)

        return ppl

    @staticmethod
    def infiltration(
            model: openstudio.openstudiomodel.Model,
            space_type: openstudio.openstudiomodel.SpaceType = None,
            calculation_methods: int = 5,
            flow_rate: float = 0.000226568446,
            schedule: openstudio.openstudiomodel.ScheduleRuleset = None):

        """
        -Calculation_methods: \n
        1.Flow/Space 2.Flow/Area 3.Flow/ExteriorWallArea 4.AirChanges/Hour 5.Flow/ExteriorArea \n
        (Default is 5)
        """

        infiltration = SpaceInfiltrationDesignFlowRate(model)

        if space_type is not None:
            infiltration.setSpaceType(space_type)

        match calculation_methods:
            case 1:
                infiltration.setDesignFlowRate(flow_rate)
            case 2:
                infiltration.setFlowperSpaceFloorArea(flow_rate)
            case 3:
                infiltration.setFlowperExteriorWallArea(flow_rate)
            case 4:
                infiltration.setAirChangesperHour(flow_rate)
            case 5 | _:
                infiltration.setFlowperExteriorSurfaceArea(flow_rate)

        if schedule is not None:
            infiltration.setSchedule(schedule)

        return infiltration

    @staticmethod
    def outdoor_air(
            model: openstudio.openstudiomodel.Model,
            space_type: openstudio.openstudiomodel.SpaceType = None,
            outdoor_air_per_floor_area: float = 0,
            outdoor_air_per_person: float = 0,
            schedule: openstudio.openstudiomodel.ScheduleRuleset = None):

        outdoor_air = DesignSpecificationOutdoorAir(model)
        if space_type is not None:
            outdoor_air.setName(space_type.nameString() + "_DSOA")
        else:
            outdoor_air.setName("DSOA")
        outdoor_air.setOutdoorAirMethod("Sum")
        outdoor_air.setOutdoorAirFlowperFloorArea(outdoor_air_per_floor_area)
        outdoor_air.setOutdoorAirFlowperPerson(outdoor_air_per_person)

        if schedule is not None:
            outdoor_air.setOutdoorAirFlowRateFractionSchedule(schedule)

        if space_type is not None:
            space_type.setDesignSpecificationOutdoorAir(outdoor_air)

        return outdoor_air

    @staticmethod
    def water_use_equipment(
            model: openstudio.openstudiomodel.Model,
            peak_flow_rate: float = 0.000525,
            target_temp: float = 135,
            space: openstudio.openstudiomodel.Space = None,
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
            outdoor_air_per_person=None,
            gas_equipment=None,
            people_density_unit=None):

        """
        -People_density_unit: \n
        1.ppl (number of people) \n
        2.m2/ppl (square meter per people) \n
        3.ppl/m2 (people per square meter) \n
        (Default is 3)
        """

        ppl_density_units = {1: "People", 2: "Area/Person", 3: "Person/Area"}

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
                        print("Cannot find equipment value for space {}".format(space))
                else:
                    load_dict["equipment"] = None

                if people_density is not None and isinstance(people_density, list):
                    try:
                        load_dict["people_density"] = people_density[i]
                    except IndexError:
                        load_dict["people_density"] = None
                        print("Cannot find people density value for space {}".format(space))
                else:
                    load_dict["people_density"] = None

                if people_density_unit is not None:
                    if isinstance(people_density_unit, int):
                        load_dict["people_density_method"] = ppl_density_units[people_density_unit]
                    elif isinstance(people_density_unit, list):
                        try:
                            load_dict["people_density_method"] = ppl_density_units[people_density_unit[i]]
                        except IndexError:
                            load_dict["people_density_method"] = None
                            print("Cannot find people density unit type for space {}".format(space))
                    else:
                        raise TypeError("Invalid input type of people density unit")
                else:
                    load_dict["people_density_method"] = None

                if people_activity_level is not None and isinstance(people_activity_level, list):
                    try:
                        load_dict["people_activity_level"] = people_activity_level[i]
                    except IndexError:
                        load_dict["people_activity_level"] = None
                        print("Cannot find people activity level value for space {}".format(space))
                else:
                    load_dict["people_activity_level"] = None

                if outdoor_air_per_area is not None and isinstance(outdoor_air_per_area, list):
                    try:
                        load_dict["outdoor_air_per_area"] = outdoor_air_per_area[i]
                    except IndexError:
                        load_dict["outdoor_air_per_area"] = None
                        print("Cannot find outdoor_air_per_area value for space {}".format(space))
                else:
                    load_dict["outdoor_air_per_area"] = None

                if outdoor_air_per_person is not None and isinstance(outdoor_air_per_person, list):
                    try:
                        load_dict["outdoor_air_per_person"] = outdoor_air_per_person[i]
                    except IndexError:
                        load_dict["outdoor_air_per_person"] = None
                        print("Cannot find outdoor_air_per_person value for space {}".format(space))
                else:
                    load_dict["outdoor_air_per_person"] = None

                if gas_equipment is not None and isinstance(gas_equipment, list):
                    try:
                        load_dict["gas_power"] = gas_equipment[i]
                    except IndexError:
                        load_dict["gas_power"] = None
                        print("Cannot find gas_power value for space {}".format(space))
                else:
                    load_dict["gas_power"] = None

                internal_load[space] = load_dict

        internal_load_json = json.dumps(internal_load, indent=4)

        return internal_load_json



