import openstudio
from openstudio.openstudiomodel import Space, SpaceType, ThermalZone, BuildingStory
from openstudio.openstudiomodel import Lights, ElectricEquipment, People
from openstudio.openstudiomodel import GasEquipment, InternalMass
from openstudio.openstudiomodel import LightsDefinition, ElectricEquipmentDefinition, PeopleDefinition
from openstudio.openstudiomodel import GasEquipmentDefinition
from openstudio.openstudiomodel import DesignSpecificationOutdoorAir, SpaceInfiltrationDesignFlowRate
from openstudio.openstudiomodel import Construction


class ZoneTool:

    # Create a thermal zone
    # @staticmethod
    # def thermal_zone(
    #         model,
    #         name,
    #         cooling_setpoint_schedules=[],
    #         heating_setpoint_schedules=[],
    #         dehumidification_setpoint_schedules=[],
    #         humidification_setpoint_schedules=[],
    #         multiplier: int = None,
    #         ceiling_height=None,
    #         volume=None,
    #         zone_inside_convention_algorithm: str = None,
    #         zone_outside_convention_algorithm: str = None,
    #         use_ideal_air_load: bool = False):
    #
    #     zone = ThermalZone(model)
    #     zone.setName(name)
    #
    #     # Assign thermostats to the zone:
    #     thermostat = openstudio.openstudiomodel.ThermostatSetpointDualSetpoint(model)
    #     if cooling_setpoint_schedules is not None and len(cooling_setpoint_schedules) != 0:
    #         if len(cooling_setpoint_schedules) == len(spaces):
    #             thermostat.setCoolingSchedule(cooling_setpoint_schedules[i])
    #         else:
    #             thermostat.setCoolingSchedule(cooling_setpoint_schedules[0])
    #     if heating_setpoint_schedules is not None and len(heating_setpoint_schedules) != 0:
    #         if len(heating_setpoint_schedules) == len(spaces):
    #             thermostat.setHeatingSchedule(heating_setpoint_schedules[i])
    #         else:
    #             thermostat.setHeatingSchedule(heating_setpoint_schedules[0])
    #
    #     # Assign humidity thermostat to the zone:
    #     humidity_thermostat = openstudio.openstudiomodel.ZoneControlHumidistat(model)
    #     if dehumidification_setpoint_schedules is not None and len(dehumidification_setpoint_schedules) != 0:
    #         if len(dehumidification_setpoint_schedules) == len(spaces):
    #             humidity_thermostat.setDehumidifyingRelativeHumiditySetpointSchedule(
    #                 dehumidification_setpoint_schedules[i])
    #         else:
    #             humidity_thermostat.setDehumidifyingRelativeHumiditySetpointSchedule(
    #                 cooling_setpoint_schedules[0])
    #     if humidification_setpoint_schedules is not None and len(humidification_setpoint_schedules) != 0:
    #         if len(humidification_setpoint_schedules) == len(spaces):
    #             humidity_thermostat.setHumidifyingRelativeHumiditySetpointSchedule(
    #                 humidification_setpoint_schedules[i])
    #         else:
    #             humidity_thermostat.setHumidifyingRelativeHumiditySetpointSchedule(
    #                 humidification_setpoint_schedules[0])
    #
    #     # Set other properties:
    #     if multiplier is not None:
    #         zone.setMultiplier(multiplier)
    #     if ceiling_height is not None:
    #         zone.setCeilingHeight(ceiling_height)
    #     if volume is not None:
    #         zone.setVolume(volume)
    #     if zone_inside_convention_algorithm is not None:
    #         zone.setZoneInsideConvectionAlgorithm(zone_inside_convention_algorithm)
    #     if zone_outside_convention_algorithm is not None:
    #         zone.setZoneOutsideConvectionAlgorithm(zone_outside_convention_algorithm)
    #
    #     zone.setUseIdealAirLoads(use_ideal_air_load)
    #
    #     return zone

    @staticmethod
    def thermal_zone_from_space(
            model,
            spaces,
            cooling_setpoint_schedules: openstudio.openstudiomodel.ScheduleRuleset = None,
            heating_setpoint_schedules: openstudio.openstudiomodel.ScheduleRuleset = None,
            dehumidification_setpoint_schedules: openstudio.openstudiomodel.ScheduleRuleset = None,
            humidification_setpoint_schedules: openstudio.openstudiomodel.ScheduleRuleset = None,
            multiplier: int = None,
            ceiling_height=None,
            volume=None,
            zone_inside_convention_algorithm: int = None,
            zone_outside_convention_algorithm: int = None,
            use_ideal_air_load: bool = False):

        """
        -Zone_inside_convention_algorithm: \n
        1.Simple 2.TARP 3.CeilingDiffuser 4.AdaptiveConvectionAlgorithm 5.TrombeWall 6.ASTMC1340

        -Zone_outside_convention_algorithm: \n
        1.SimpleCombined 2.TARP 3.DOE-2 4.MoWiTT 5.AdaptiveConvectionAlgorithm
        """

        inside_algorithms = {1: "Simple", 2: "TARP", 3: "CeilingDiffuser",
                             4: "AdaptiveConvectionAlgorithm", 5: "TrombeWall", 6: "ASTMC1340"}

        outside_algorithms = {1: "SimpleCombined", 2: "TARP", 3: "DOE-2",
                              4: "MoWiTT", 5: "AdaptiveConvectionAlgorithm"}

        thermal_zones = []
        if spaces is not None:
            if isinstance(spaces, openstudio.openstudiomodel.Space):
                zone = ThermalZone(model)
                zone.setName(spaces.nameString())
                spaces.setThermalZone(zone)

                # Assign thermostats to the zone:
                thermostat = openstudio.openstudiomodel.ThermostatSetpointDualSetpoint(model)
                if cooling_setpoint_schedules is not None:
                    thermostat.setCoolingSchedule(cooling_setpoint_schedules)
                if heating_setpoint_schedules is not None:
                    thermostat.setHeatingSchedule(heating_setpoint_schedules)

                zone.setThermostatSetpointDualSetpoint(thermostat)

                # Assign humidity thermostat to the zone:
                humidity_thermostat = openstudio.openstudiomodel.ZoneControlHumidistat(model)
                if dehumidification_setpoint_schedules is not None:
                    humidity_thermostat.setDehumidifyingRelativeHumiditySetpointSchedule(
                        dehumidification_setpoint_schedules)
                if humidification_setpoint_schedules is not None:
                    humidity_thermostat.setHumidifyingRelativeHumiditySetpointSchedule(
                        humidification_setpoint_schedules)

                zone.setZoneControlHumidistat(humidity_thermostat)

                # Set other properties:
                if multiplier is not None:
                    zone.setMultiplier(multiplier)
                if ceiling_height is not None:
                    zone.setCeilingHeight(ceiling_height)
                if volume is not None:
                    zone.setVolume(volume)
                if zone_inside_convention_algorithm is not None:
                    zone.setZoneInsideConvectionAlgorithm(inside_algorithms[zone_inside_convention_algorithm])
                if zone_outside_convention_algorithm is not None:
                    zone.setZoneOutsideConvectionAlgorithm(
                        outside_algorithms[zone_outside_convention_algorithm])

                zone.setUseIdealAirLoads(use_ideal_air_load)

                return zone

            elif isinstance(spaces, list):
                for i, space in enumerate(spaces):
                    zone = ThermalZone(model)
                    zone.setName(space.nameString())
                    space.setThermalZone(zone)

                    # Assign thermostats to the zone:
                    thermostat = openstudio.openstudiomodel.ThermostatSetpointDualSetpoint(model)
                    if cooling_setpoint_schedules is not None:
                        if isinstance(cooling_setpoint_schedules, openstudio.openstudiomodel.ScheduleRuleset):
                            thermostat.setCoolingSchedule(cooling_setpoint_schedules)
                        elif isinstance(cooling_setpoint_schedules, list):
                            thermostat.setCoolingSchedule(cooling_setpoint_schedules[i])
                        else:
                            raise TypeError("Invalid input type of cooling_setpoint_schedules")
                    if heating_setpoint_schedules is not None:
                        if isinstance(heating_setpoint_schedules, openstudio.openstudiomodel.ScheduleRuleset):
                            thermostat.setHeatingSchedule(heating_setpoint_schedules)
                        elif isinstance(heating_setpoint_schedules, list):
                            thermostat.setHeatingSchedule(heating_setpoint_schedules[i])
                        else:
                            raise TypeError("Invalid input type of heating_setpoint_schedules")

                    zone.setThermostatSetpointDualSetpoint(thermostat)

                    # Assign humidity thermostat to the zone:
                    humidity_thermostat = openstudio.openstudiomodel.ZoneControlHumidistat(model)
                    if dehumidification_setpoint_schedules is not None:
                        if isinstance(dehumidification_setpoint_schedules, openstudio.openstudiomodel.ScheduleRuleset):
                            humidity_thermostat.setDehumidifyingRelativeHumiditySetpointSchedule(
                                dehumidification_setpoint_schedules)
                        elif isinstance(dehumidification_setpoint_schedules, list):
                            humidity_thermostat.setDehumidifyingRelativeHumiditySetpointSchedule(
                                cooling_setpoint_schedules[i])
                        else:
                            raise TypeError("Invalid input type of dehumidification_setpoint_schedules")
                    if humidification_setpoint_schedules is not None:
                        if isinstance(humidification_setpoint_schedules, openstudio.openstudiomodel.ScheduleRuleset):
                            humidity_thermostat.setHumidifyingRelativeHumiditySetpointSchedule(
                                humidification_setpoint_schedules)
                        elif isinstance(humidification_setpoint_schedules, list):
                            humidity_thermostat.setHumidifyingRelativeHumiditySetpointSchedule(
                                humidification_setpoint_schedules[i])
                        else:
                            raise TypeError("Invalid input type of humidification_setpoint_schedules")

                    zone.setZoneControlHumidistat(humidity_thermostat)

                    # Set other properties:
                    if multiplier is not None:
                        zone.setMultiplier(multiplier)
                    if ceiling_height is not None:
                        zone.setCeilingHeight(ceiling_height)
                    if volume is not None:
                        zone.setVolume(volume)
                    if zone_inside_convention_algorithm is not None:
                        zone.setZoneInsideConvectionAlgorithm(inside_algorithms[zone_inside_convention_algorithm])
                    if zone_outside_convention_algorithm is not None:
                        zone.setZoneOutsideConvectionAlgorithm(outside_algorithms[zone_outside_convention_algorithm])

                    zone.setUseIdealAirLoads(use_ideal_air_load)
                    thermal_zones.append(zone)

                return thermal_zones

            else:
                raise TypeError("Invalid input type of spaces")

    @staticmethod
    def sizing(
            model: openstudio.openstudiomodel.Model,
            thermal_zone: openstudio.openstudiomodel.ThermalZone,
            cooling_design_supply_air_temp_input_method: int = 1,
            cooling_design_supply_air_temp=None,
            cooling_design_supply_air_temp_diff=None,
            heating_design_supply_air_temp_input_method: int = 1,
            heating_design_supply_air_temp=None,
            heating_design_supply_air_temp_diff=None,
            cooling_design_supply_air_humidity_ratio=None,
            heating_design_supply_air_humidity_ratio=None,
            cooling_sizing_factor=None,
            heating_sizing_factor=None,
            cooling_design_air_flow_method: int = 2,
            cooling_design_air_flow=None,
            cooling_min_air_flow=None,
            cooling_min_air_flow_per_floor_area=None,
            cooling_min_air_flow_fraction=None,
            heating_design_air_flow_method: int = 2,
            heating_design_air_flow=None,
            heating_max_air_flow=None,
            heating_max_air_flow_per_floor_area=None,
            heating_max_air_flow_fraction=None,
            account_for_doas: bool = False,
            doas_control_strategy: int = 1,
            doas_low_setpoint=None,
            doas_high_setpoint=None,
            zone_load_sizing_method: int = 3,
            latent_cooling_design_supply_air_humidity_ratio_input_method: int = 1,
            dehumidification_design_supply_air_humidity_ratio=None,
            cooling_design_supply_air_humidity_ratio_diff=None,
            latent_heating_design_supply_air_humidity_ratio_input_method: int = 1,
            humidification_design_supply_air_humidity_ratio=None,
            humidification_design_supply_air_humidity_ratio_diff=None,
            dehumidification_setpoint_schedule=None,
            humidification_setpoint_schedule=None,
            air_distribution_effectiveness_cooling=None,
            air_distribution_effectiveness_heating=None,
            secondary_recirculation_fraction=None,
            min_ventilation_efficiency=None):

        """
        -Cooling_design_supply_air_temp_input_method: 1.SupplyAirTemperature 2.TemperatureDifference \n
        -Heating_design_supply_air_temp_input_method: 1.SupplyAirTemperature 2.TemperatureDifference \n
        -Cooling_design_air_flow_method: 1.Flow/Zone 2.DesignDay 3.DesignDayWithLimit \n
        -Heating_design_air_flow_method: 1.Flow/Zone 2.DesignDay 3.DesignDayWithLimit \n
        -Doas_control_strategy: 1.NeutralSupplyAir 2.NeutralDehumidifiedSupplyAir 3.ColdSupplyAir \n
        -Zone_load_sizing_method: \n
        1.Sensible Load 2.Latent Load 3.Sensible And Latent Load 4.Sensible Load Only No Latent Load \n
        -Latent_cooling_design_supply_air_humidity_ratio_input_method:
        1.SupplyAirHumidityRatio 2.HumidityRatioDifference \n
        -Latent_heating_design_supply_air_humidity_ratio_input_method:
        1.SupplyAirHumidityRatio 2.HumidityRatioDifference
        """

        air_temp_methods = {1: "SupplyAirTemperature", 2: "TemperatureDifference"}
        air_flow_methods = {1: "Flow/Zone", 2: "DesignDay", 3: "DesignDayWithLimit"}
        doas_strategies = {1: "NeutralSupplyAir", 2: "NeutralDehumidifiedSupplyAir", 3: "ColdSupplyAir"}
        zone_load_methods = {1: "Sensible Load", 2: "Latent Load",
                             3: "Sensible And Latent Load", 4: "Sensible Load Only No Latent Load"}
        humidity_methods = {1: "SupplyAirHumidityRatio", 2: "HumidityRatioDifference"}

        sizing = openstudio.openstudiomodel.SizingZone(model, thermal_zone)

        sizing.setZoneCoolingDesignSupplyAirTemperatureInputMethod(
            air_temp_methods[cooling_design_supply_air_temp_input_method])
        if cooling_design_supply_air_temp is not None:
            sizing.setZoneCoolingDesignSupplyAirTemperature(cooling_design_supply_air_temp)
        if cooling_design_supply_air_temp_diff is not None:
            sizing.setZoneCoolingDesignSupplyAirTemperatureDifference(cooling_design_supply_air_temp_diff)

        sizing.setZoneHeatingDesignSupplyAirTemperatureInputMethod(
            air_temp_methods[heating_design_supply_air_temp_input_method])
        if heating_design_supply_air_temp is not None:
            sizing.setZoneHeatingDesignSupplyAirTemperature(heating_design_supply_air_temp)
        if heating_design_supply_air_temp_diff is not None:
            sizing.setZoneHeatingDesignSupplyAirTemperatureDifference(heating_design_supply_air_temp_diff)

        if cooling_design_supply_air_humidity_ratio is not None:
            sizing.setZoneCoolingDesignSupplyAirHumidityRatio(cooling_design_supply_air_humidity_ratio)
        if heating_design_supply_air_humidity_ratio is not None:
            sizing.setZoneHeatingDesignSupplyAirHumidityRatio(heating_design_supply_air_humidity_ratio)

        if cooling_sizing_factor is not None:
            sizing.setZoneCoolingSizingFactor(cooling_sizing_factor)
        if heating_sizing_factor is not None:
            sizing.setZoneHeatingSizingFactor(heating_sizing_factor)

        sizing.setCoolingDesignAirFlowMethod(air_flow_methods[cooling_design_air_flow_method])
        if cooling_design_air_flow is not None:
            sizing.setCoolingDesignAirFlowRate(cooling_design_air_flow)
        if cooling_min_air_flow is not None:
            sizing.setCoolingMinimumAirFlow(cooling_min_air_flow)
        if cooling_min_air_flow_per_floor_area is not None:
            sizing.setCoolingMinimumAirFlowperZoneFloorArea(cooling_min_air_flow_per_floor_area)
        if cooling_min_air_flow_fraction is not None:
            sizing.setCoolingMinimumAirFlowFraction(cooling_min_air_flow_fraction)

        sizing.setHeatingDesignAirFlowMethod(air_flow_methods[heating_design_air_flow_method])
        if heating_design_air_flow is not None:
            sizing.setHeatingDesignAirFlowRate(heating_design_air_flow)
        if heating_max_air_flow is not None:
            sizing.setHeatingMaximumAirFlow(heating_max_air_flow)
        if heating_max_air_flow_per_floor_area is not None:
            sizing.setHeatingMaximumAirFlowperZoneFloorArea(heating_max_air_flow_per_floor_area)
        if heating_max_air_flow_fraction is not None:
            sizing.setHeatingMaximumAirFlowFraction(heating_max_air_flow_fraction)

        if account_for_doas is not None:
            sizing.setAccountforDedicatedOutdoorAirSystem(account_for_doas)

        sizing.setDedicatedOutdoorAirSystemControlStrategy(doas_strategies[doas_control_strategy])

        if doas_low_setpoint is not None:
            sizing.setDedicatedOutdoorAirLowSetpointTemperatureforDesign(doas_low_setpoint)
        if doas_high_setpoint is not None:
            sizing.setDedicatedOutdoorAirHighSetpointTemperatureforDesign(doas_high_setpoint)

        sizing.setZoneLoadSizingMethod(zone_load_methods[zone_load_sizing_method])

        sizing.setZoneLatentCoolingDesignSupplyAirHumidityRatioInputMethod(
            humidity_methods[latent_cooling_design_supply_air_humidity_ratio_input_method])

        if dehumidification_design_supply_air_humidity_ratio is not None:
            sizing.setZoneDehumidificationDesignSupplyAirHumidityRatio(
                dehumidification_design_supply_air_humidity_ratio)
        if cooling_design_supply_air_humidity_ratio_diff is not None:
            sizing.setZoneCoolingDesignSupplyAirHumidityRatioDifference(
                cooling_design_supply_air_humidity_ratio_diff)

        sizing.setZoneLatentHeatingDesignSupplyAirHumidityRatioInputMethod(
            humidity_methods[latent_heating_design_supply_air_humidity_ratio_input_method])

        if humidification_design_supply_air_humidity_ratio is not None:
            sizing.setZoneHumidificationDesignSupplyAirHumidityRatio(
                humidification_design_supply_air_humidity_ratio)
        if humidification_design_supply_air_humidity_ratio_diff is not None:
            sizing.setZoneHumidificationDesignSupplyAirHumidityRatioDifference(
                humidification_design_supply_air_humidity_ratio_diff)

        if dehumidification_setpoint_schedule is not None:
            sizing.setZoneHumidistatDehumidificationSetPointSchedule(dehumidification_setpoint_schedule)
        if humidification_setpoint_schedule is not None:
            sizing.setZoneHumidistatHumidificationSetPointSchedule(humidification_setpoint_schedule)

        if air_distribution_effectiveness_cooling is not None:
            sizing.setDesignZoneAirDistributionEffectivenessinCoolingMode(air_distribution_effectiveness_cooling)
        if air_distribution_effectiveness_heating is not None:
            sizing.setDesignZoneAirDistributionEffectivenessinHeatingMode(air_distribution_effectiveness_heating)

        if secondary_recirculation_fraction is not None:
            sizing.setDesignZoneSecondaryRecirculationFraction(secondary_recirculation_fraction)
        if min_ventilation_efficiency is not None:
            sizing.setDesignMinimumZoneVentilationEfficiency(min_ventilation_efficiency)

        return sizing

    # Create a space with full set of information:
    @staticmethod
    def space_simplified(
            model,
            name,
            program,
            thermal_zone=None,
            story=None,
            lighting_power=0,
            equipment_power=0,
            people_density=0,
            gas_power=0,
            outdoor_air_per_floor_area=0,
            outdoor_air_per_person=0,
            internal_mass: InternalMass = None,
            lighting_schedule=None,
            equipment_schedule=None,
            occupancy_schedule=None,
            activity_schedule=None,
            infiltration_schedule=None,
            gas_schedule=None):

        space = Space(model)
        space.setName(name)
        if thermal_zone is not None:
            space.setThermalZone(thermal_zone)
        if story is not None:
            space.setBuildingStory(story)

        # Define internal load objects:
        # Lighting:
        lighting_def = LightsDefinition(model)
        lighting_def.setWattsperSpaceFloorArea(lighting_power)
        light = Lights(lighting_def)
        if lighting_schedule is not None:
            light.setSchedule(lighting_schedule)
        light.setSpace(space)

        # Equipment:
        equipment_def = ElectricEquipmentDefinition(model)
        equipment_def.setWattsperSpaceFloorArea(equipment_power)
        equipment = ElectricEquipment(equipment_def)
        if equipment_schedule is not None:
            equipment.setSchedule(equipment_schedule)
        equipment.setSpace(space)

        # People:
        people_def = PeopleDefinition(model)
        people_def.setPeopleperSpaceFloorArea(people_density)
        people = People(people_def)
        if occupancy_schedule is not None:
            people.setNumberofPeopleSchedule(occupancy_schedule)
        if activity_schedule is not None:
            people.setActivityLevelSchedule(activity_schedule)
        people.setSpace(space)

        # Gas Equipment:
        if gas_power is not None and gas_power != 0:
            gas_def = GasEquipmentDefinition(model)
            gas_def.setWattsperSpaceFloorArea(gas_power)
            gas = GasEquipment(gas_def)
            if gas_schedule is not None:
                gas.setSchedule(gas_schedule)
            gas.setSpace(space)

        # Internal mass:
        if internal_mass is not None:
            internal_mass.setSpace(space)

        # Space Type:
        space_type = SpaceType(model)
        space_type.setName(program + ":" + name)

        # Outdoor Air:
        outdoor_air = DesignSpecificationOutdoorAir(model)
        outdoor_air.setName(name + "_DSOA")
        outdoor_air.setOutdoorAirMethod("Sum")
        outdoor_air.setOutdoorAirFlowperFloorArea(outdoor_air_per_floor_area)
        outdoor_air.setOutdoorAirFlowperPerson(outdoor_air_per_person)
        if occupancy_schedule is not None:
            outdoor_air.setOutdoorAirFlowRateFractionSchedule(occupancy_schedule)

        space_type.setDesignSpecificationOutdoorAir(outdoor_air)

        # Infiltration Flow Rate:
        infiltration = SpaceInfiltrationDesignFlowRate(model)
        infiltration.setSpaceType(space_type)
        infiltration.setFlowperExteriorSurfaceArea(0.000226568446)
        if infiltration_schedule is not None:
            infiltration.setSchedule(infiltration_schedule)

        # Apply space type:
        space.setSpaceType(space_type)

        return space

    @staticmethod
    def space_type(
            model: openstudio.openstudiomodel.Model,
            name: str,
            program: str,
            outdoor_air: DesignSpecificationOutdoorAir = None,
            infiltration: SpaceInfiltrationDesignFlowRate = None):

        space_type = SpaceType(model)
        space_type.setName(program + ":" + name)

        if outdoor_air is not None:
            space_type.setDesignSpecificationOutdoorAir(outdoor_air)
        if infiltration is not None:
            infiltration.setSpaceType(space_type)

        return space_type

    @staticmethod
    def space(
            model: openstudio.openstudiomodel.Model,
            space_type: openstudio.openstudiomodel.SpaceType,
            name: str,
            thermal_zone: ThermalZone = None,
            story: BuildingStory = None,
            lights: Lights = None,
            people: People = None,
            electric_equipment: ElectricEquipment = None,
            gas_equipment: GasEquipment = None,
            internal_mass: InternalMass = None):

        space = Space(model)
        space.setName(name)
        if thermal_zone is not None:
            space.setThermalZone(thermal_zone)
        if story is not None:
            space.setBuildingStory(story)

        if lights is not None:
            lights.setSpace(space)
        if people is not None:
            people.setSpace(space)
        if electric_equipment is not None:
            electric_equipment.setSpace(space)
        if gas_equipment is not None:
            gas_equipment.setSpace(space)
        if internal_mass is not None:
            internal_mass.setSpace(space)

        # Space Type:
        if space_type is not None:
            space.setSpaceType(space_type)

        return space

    @staticmethod
    def get_thermal_zone(thermal_zones: list):
        """
        -thermal_zones: a list of thermal zone dictionary objects. Use output from "geometry_from_json" here.
        """

        zones = []
        for zone_dict in thermal_zones:
            zones.append(zone_dict["zone"])

        return zones

    @staticmethod
    def thermal_zone_by_floor(thermal_zones: list, sub_sort_by_type: bool = False):
        """
        :param thermal_zones: a list of thermal zone dictionary objects. Use output from "geometry_from_json" here.
        :param sub_sort_by_type: set to True to sort thermal zones based on their type on each floor. Default is False.
        :return: a dictionary of sorted thermal zones.
        """

        if thermal_zones is not None:
            sorted_zones = {}
            if sub_sort_by_type:
                # First building dictionary structure:
                for zone_dict in thermal_zones:
                    keys = sorted_zones.keys()
                    story = zone_dict["story"]
                    if story not in keys:
                        sorted_zones[story] = {}
                story_keys = sorted_zones.keys()

                # Then add thermal zone sorted by space type to each story:
                for zone_dict in thermal_zones:

                    zone = zone_dict["zone"]
                    story = zone_dict["story"]
                    space_type = zone_dict["space_type"]

                    if story in story_keys:
                        story_dict = sorted_zones[story]
                        type_keys = story_dict.keys()

                        if space_type not in type_keys:
                            story_dict[space_type] = [zone]
                        else:
                            zones = story_dict[space_type]
                            zones.append(zone)

            else:
                for zone_dict in thermal_zones:
                    story_keys = sorted_zones.keys()

                    zone = zone_dict["zone"]
                    story = zone_dict["story"]

                    if story not in story_keys:
                        sorted_zones[story] = [zone]
                    else:
                        zones = sorted_zones[story]
                        zones.append(zone)

            return sorted_zones

    @staticmethod
    def thermal_zone_by_type(thermal_zones: list):
        """
        :param thermal_zones: a list of thermal zone dictionary objects. Use output from "geometry_from_json" here.
        :return: a dictionary of sorted thermal zones.
        """

        if thermal_zones is not None:
            sorted_zones = {}
            for zone_dict in thermal_zones:
                type_keys = sorted_zones.keys()

                zone = zone_dict["zone"]
                space_type = zone_dict["space_type"]

                if space_type not in type_keys:
                    sorted_zones[space_type] = [zone]
                else:
                    zones = sorted_zones[space_type]
                    zones.append(zone)

            return sorted_zones

    @staticmethod
    def thermal_zone_by_name(thermal_zones: list, name_to_search: str):
        """
        :param thermal_zones: a list of thermal zone dictionary objects. Use output from "geometry_from_json" here.
        :param name_to_search: zone name to search for.
        :return: a list of target thermal zones.
        """

        target_zones = []
        for zone_dict in thermal_zones:
            zone_name = zone_dict["name"]

            if name_to_search in zone_name:
                target_zones.append(zone_dict["zone"])

        return target_zones

    @staticmethod
    def thermal_zone_by_conditioned(thermal_zones: list):
        """
        :param thermal_zones: a list of thermal zone dictionary objects. Use output from "geometry_from_json" here.
        :return: a list of conditioned zone dictionary objects and unconditioned zone dictionary objects.
        """

        conditioned_zones = []
        unconditioned_zones = []
        for zone_dict in thermal_zones:
            condition = zone_dict["conditioned"]

            if condition:
                conditioned_zones.append(zone_dict)
            else:
                unconditioned_zones.append(zone_dict)

        return conditioned_zones, unconditioned_zones

    @staticmethod
    def construction_by_orientation(
            sorted_surfaces: dict,
            construction_east: Construction = None,
            construction_west: Construction = None,
            construction_north: Construction = None,
            construction_south: Construction = None,
            construction_default: Construction = None):

        """
        sorted_surfaces: A dictionary of surfaces. Use output from "geometry_from_json" here.
        """

        for key in sorted_surfaces.keys():
            match key:
                case "east":
                    if construction_east is not None and len(sorted_surfaces[key]) != 0:
                        for srf in sorted_surfaces[key]:
                            srf.setConstruction(construction_east)
                case "west":
                    if construction_west is not None and len(sorted_surfaces[key]) != 0:
                        for srf in sorted_surfaces[key]:
                            srf.setConstruction(construction_west)
                case "north":
                    if construction_north is not None and len(sorted_surfaces[key]) != 0:
                        for srf in sorted_surfaces[key]:
                            srf.setConstruction(construction_north)
                case "south":
                    if construction_south is not None and len(sorted_surfaces[key]) != 0:
                        for srf in sorted_surfaces[key]:
                            srf.setConstruction(construction_south)
                case _:
                    if construction_default is not None and len(sorted_surfaces[key]) != 0:
                        for srf in sorted_surfaces[key]:
                            srf.setConstruction(construction_default)

    @staticmethod
    def multiplier_by_floor(thermal_zone, multiplier: int = 1):

        if isinstance(thermal_zone, openstudio.openstudiomodel.ThermalZone):
            thermal_zone.setMultiplier(multiplier)
        elif isinstance(thermal_zone, list):
            for zone in thermal_zone:
                if isinstance(zone, openstudio.openstudiomodel.ThermalZone):
                    zone.setMultiplier(multiplier)
        else:
            raise TypeError("Invalid input type of thermal zone")

    @staticmethod
    def add_window_by_ratio(
            sorted_surfaces: dict,
            glz_ratio,
            surface_type: int = 1,
            construction=None,
            height_offset: float = 0.1,
            offset_from_floor: bool = True):

        """
        - sorted_surfaces: A dictionary of surfaces. Use output from "geometry_from_json" here. \n
        - glz_ratio: A float number to be applied to all surfaces or a dictionary of numbers for each orientation. \n
        - construction: A single construction to be applied to all surfaces object or a dictionary of construction for each orientation
        - Surface_type: 1.FixedWindow 2.OperableWindow 3.GlassDoor 4.Door 5.OverheadDoor 6.Skylight 7.TubularDaylightDome 8.TubularDaylightDiffuser
        """

        types = {1: "FixedWindow", 2: "OperableWindow", 3: "GlassDoor", 4: "Door", 5: "OverheadDoor", 6: "Skylight",
                 7: "TubularDaylightDome", 8: "TubularDaylightDiffuser"}

        sub_srfs = []
        for key in sorted_surfaces.keys():
            if len(sorted_surfaces[key]) != 0:
                if isinstance(glz_ratio, dict):
                    ratio = glz_ratio[key]
                elif isinstance(glz_ratio, float):
                    ratio = glz_ratio
                else:
                    raise TypeError("Invalid type of glz_ratio.")

                for srf in sorted_surfaces[key]:
                    win = srf.setWindowToWallRatio(ratio, height_offset, offset_from_floor).get()
                    win.setSubSurfaceType(types[surface_type])

                    if construction is not None:
                        if isinstance(construction, dict):
                            cons = construction[key]
                        elif isinstance(construction, Construction):
                            cons = construction
                        else:
                            raise TypeError("Invalid type of construction.")
                        win.setConstruction(cons)

                    sub_srfs.append(win)

        return sub_srfs

    @staticmethod
    def adiabatic_by_type(
            thermal_zone,
            walls: bool = False,
            interior_walls: bool = False,
            air_walls: bool = False,
            windows: bool = False,
            interior_windows: bool = False,
            roofs: bool = False,
            ceilings: bool = False,
            floors: bool = False,
            exposed_floors: bool = False,
            ground_floors: bool = False,
            underground_walls: bool = False,
            underground_slabs: bool = False,
            underground_ceiling: bool = False):

        if isinstance(thermal_zone, openstudio.openstudiomodel.ThermalZone):
            space = thermal_zone.spaces()[0]
            surfaces = space.surfaces()

            # thermal_zone.setMultiplier(multiplier)
        elif isinstance(thermal_zone, list):
            for zone in thermal_zone:
                if isinstance(zone, openstudio.openstudiomodel.ThermalZone):
                    pass
                    # zone.setMultiplier(multiplier)
        else:
            raise TypeError("Invalid input type of thermal zone")
