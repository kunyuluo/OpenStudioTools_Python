import openstudio
from openstudio.openstudiomodel import Space, SpaceType, ThermalZone, BuildingStory
from openstudio.openstudiomodel import Lights, ElectricEquipment, People
from openstudio.openstudiomodel import GasEquipment, InternalMass
from openstudio.openstudiomodel import LightsDefinition, ElectricEquipmentDefinition, PeopleDefinition
from openstudio.openstudiomodel import GasEquipmentDefinition, InternalMassDefinition
from openstudio.openstudiomodel import DesignSpecificationOutdoorAir, SpaceInfiltrationDesignFlowRate
from Schedules.Templates.Template import Office


class ZoneTool:

    # Create a thermal zone
    @staticmethod
    def thermal_zone(
            model,
            name,
            cooling_setpoint_schedules=[],
            heating_setpoint_schedules=[],
            dehumidification_setpoint_schedules=[],
            humidification_setpoint_schedules=[],
            multiplier: int = None,
            ceiling_height=None,
            volume=None,
            zone_inside_convention_algorithm: str = None,
            zone_outside_convention_algorithm: str = None,
            use_ideal_air_load: bool = False):

        zone = ThermalZone(model)
        zone.setName(name)

        # Assign thermostats to the zone:
        thermostat = openstudio.openstudiomodel.ThermostatSetpointDualSetpoint(model)
        if cooling_setpoint_schedules is not None and len(cooling_setpoint_schedules) != 0:
            if len(cooling_setpoint_schedules) == len(spaces):
                thermostat.setCoolingSchedule(cooling_setpoint_schedules[i])
            else:
                thermostat.setCoolingSchedule(cooling_setpoint_schedules[0])
        if heating_setpoint_schedules is not None and len(heating_setpoint_schedules) != 0:
            if len(heating_setpoint_schedules) == len(spaces):
                thermostat.setHeatingSchedule(heating_setpoint_schedules[i])
            else:
                thermostat.setHeatingSchedule(heating_setpoint_schedules[0])

        # Assign humidity thermostat to the zone:
        humidity_thermostat = openstudio.openstudiomodel.ZoneControlHumidistat(model)
        if dehumidification_setpoint_schedules is not None and len(dehumidification_setpoint_schedules) != 0:
            if len(dehumidification_setpoint_schedules) == len(spaces):
                humidity_thermostat.setDehumidifyingRelativeHumiditySetpointSchedule(
                    dehumidification_setpoint_schedules[i])
            else:
                humidity_thermostat.setDehumidifyingRelativeHumiditySetpointSchedule(
                    cooling_setpoint_schedules[0])
        if humidification_setpoint_schedules is not None and len(humidification_setpoint_schedules) != 0:
            if len(humidification_setpoint_schedules) == len(spaces):
                humidity_thermostat.setHumidifyingRelativeHumiditySetpointSchedule(
                    humidification_setpoint_schedules[i])
            else:
                humidity_thermostat.setHumidifyingRelativeHumiditySetpointSchedule(
                    humidification_setpoint_schedules[0])

        # Set other properties:
        if multiplier is not None:
            zone.setMultiplier(multiplier)
        if ceiling_height is not None:
            zone.setCeilingHeight(ceiling_height)
        if volume is not None:
            zone.setVolume(volume)
        if zone_inside_convention_algorithm is not None:
            zone.setZoneInsideConvectionAlgorithm(zone_inside_convention_algorithm)
        if zone_outside_convention_algorithm is not None:
            zone.setZoneOutsideConvectionAlgorithm(zone_outside_convention_algorithm)

        zone.setUseIdealAirLoads(use_ideal_air_load)

        return zone

    @staticmethod
    def thermal_zone_from_space(
            model,
            spaces=[],
            cooling_setpoint_schedules=[],
            heating_setpoint_schedules=[],
            dehumidification_setpoint_schedules=[],
            humidification_setpoint_schedules=[],
            multiplier: int = None,
            ceiling_height=None,
            volume=None,
            zone_inside_convention_algorithm: str = None,
            zone_outside_convention_algorithm: str = None,
            use_ideal_air_load: bool = False):

        thermal_zones = []
        if spaces is not None and len(spaces) != 0:
            for i in range(len(spaces)):
                zone = ThermalZone(model)
                zone.setName(spaces[i].nameString())
                spaces[i].setThermalZone(zone)

                # Assign thermostats to the zone:
                thermostat = openstudio.openstudiomodel.ThermostatSetpointDualSetpoint(model)
                if cooling_setpoint_schedules is not None and len(cooling_setpoint_schedules) != 0:
                    if len(cooling_setpoint_schedules) == len(spaces):
                        thermostat.setCoolingSchedule(cooling_setpoint_schedules[i])
                    else:
                        thermostat.setCoolingSchedule(cooling_setpoint_schedules[0])
                if heating_setpoint_schedules is not None and len(heating_setpoint_schedules) != 0:
                    if len(heating_setpoint_schedules) == len(spaces):
                        thermostat.setHeatingSchedule(heating_setpoint_schedules[i])
                    else:
                        thermostat.setHeatingSchedule(heating_setpoint_schedules[0])

                zone.setThermostatSetpointDualSetpoint(thermostat)

                # Assign humidity thermostat to the zone:
                humidity_thermostat = openstudio.openstudiomodel.ZoneControlHumidistat(model)
                if dehumidification_setpoint_schedules is not None and len(dehumidification_setpoint_schedules) != 0:
                    if len(dehumidification_setpoint_schedules) == len(spaces):
                        humidity_thermostat.setDehumidifyingRelativeHumiditySetpointSchedule(
                            dehumidification_setpoint_schedules[i])
                    else:
                        humidity_thermostat.setDehumidifyingRelativeHumiditySetpointSchedule(
                            cooling_setpoint_schedules[0])
                if humidification_setpoint_schedules is not None and len(humidification_setpoint_schedules) != 0:
                    if len(humidification_setpoint_schedules) == len(spaces):
                        humidity_thermostat.setHumidifyingRelativeHumiditySetpointSchedule(
                            humidification_setpoint_schedules[i])
                    else:
                        humidity_thermostat.setHumidifyingRelativeHumiditySetpointSchedule(
                            humidification_setpoint_schedules[0])

                zone.setZoneControlHumidistat(humidity_thermostat)

                # Set other properties:
                if multiplier is not None:
                    zone.setMultiplier(multiplier)
                if ceiling_height is not None:
                    zone.setCeilingHeight(ceiling_height)
                if volume is not None:
                    zone.setVolume(volume)
                if zone_inside_convention_algorithm is not None:
                    zone.setZoneInsideConvectionAlgorithm(zone_inside_convention_algorithm)
                if zone_outside_convention_algorithm is not None:
                    zone.setZoneOutsideConvectionAlgorithm(zone_outside_convention_algorithm)

                zone.setUseIdealAirLoads(use_ideal_air_load)
                thermal_zones.append(zone)

        return thermal_zones

    @staticmethod
    def sizing(
            model,
            thermal_zone,
            cooling_design_supply_air_temp_input_method=None,
            cooling_design_supply_air_temp=None,
            cooling_design_supply_air_temp_diff=None,
            heating_design_supply_air_temp_input_method=None,
            heating_design_supply_air_temp=None,
            heating_design_supply_air_temp_diff=None,
            cooling_design_supply_air_humidity_ratio=None,
            heating_design_supply_air_humidity_ratio=None,
            cooling_sizing_factor=None,
            heating_sizing_factor=None,
            cooling_design_air_flow_method=None,
            cooling_design_air_flow=None,
            cooling_min_air_flow=None,
            cooling_min_air_flow_per_floor_area=None,
            cooling_min_air_flow_fraction=None,
            heating_design_air_flow_method=None,
            heating_design_air_flow=None,
            heating_max_air_flow=None,
            heating_max_air_flow_per_floor_area=None,
            heating_max_air_flow_fraction=None,
            account_for_doas: bool = False,
            doas_control_strategy: str = "NeutralSupplyAir",
            doas_low_setpoint=None,
            doas_high_setpoint=None,
            zone_load_sizing_method: str = "Sensible And Latent Load",
            latent_cooling_design_supply_air_humidity_ratio_input_method: str = None,
            dehumidification_design_supply_air_humidity_ratio=None,
            cooling_design_supply_air_humidity_ratio_diff=None,
            latent_heating_design_supply_air_humidity_ratio_input_method: str = None,
            humidification_design_supply_air_humidity_ratio=None,
            humidification_design_supply_air_humidity_ratio_diff=None,
            dehumidification_setpoint_schedule=None,
            humidification_setpoint_schedule=None,
            air_distribution_effectiveness_cooling=None,
            air_distribution_effectiveness_heating=None,
            secondary_recirculation_fraction=None,
            min_ventilation_efficiency=None):

        sizing = openstudio.openstudiomodel.SizingZone(model, thermal_zone)

        if cooling_design_supply_air_temp_input_method is not None:
            sizing.setZoneCoolingDesignSupplyAirTemperatureInputMethod(cooling_design_supply_air_temp_input_method)
        if cooling_design_supply_air_temp is not None:
            sizing.setZoneCoolingDesignSupplyAirTemperature(cooling_design_supply_air_temp)
        if cooling_design_supply_air_temp_diff is not None:
            sizing.setZoneCoolingDesignSupplyAirTemperatureDifference(cooling_design_supply_air_temp_diff)

        if heating_design_supply_air_temp_input_method is not None:
            sizing.setZoneHeatingDesignSupplyAirTemperatureInputMethod(heating_design_supply_air_temp_input_method)
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

        if cooling_design_air_flow_method is not None:
            sizing.setCoolingDesignAirFlowMethod(cooling_design_air_flow_method)
        if cooling_design_air_flow is not None:
            sizing.setCoolingDesignAirFlowRate(cooling_design_air_flow)
        if cooling_min_air_flow is not None:
            sizing.setCoolingMinimumAirFlow(cooling_min_air_flow)
        if cooling_min_air_flow_per_floor_area is not None:
            sizing.setCoolingMinimumAirFlowperZoneFloorArea(cooling_min_air_flow_per_floor_area)
        if cooling_min_air_flow_fraction is not None:
            sizing.setCoolingMinimumAirFlowFraction(cooling_min_air_flow_fraction)

        if heating_design_air_flow_method is not None:
            sizing.setHeatingDesignAirFlowMethod(heating_design_air_flow_method)
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
        if doas_control_strategy is not None:
            sizing.setDedicatedOutdoorAirSystemControlStrategy(doas_control_strategy)
        if doas_low_setpoint is not None:
            sizing.setDedicatedOutdoorAirLowSetpointTemperatureforDesign(doas_low_setpoint)
        if doas_high_setpoint is not None:
            sizing.setDedicatedOutdoorAirHighSetpointTemperatureforDesign(doas_high_setpoint)

        sizing.setZoneLoadSizingMethod(zone_load_sizing_method)

        if latent_cooling_design_supply_air_humidity_ratio_input_method is not None:
            sizing.setZoneLatentCoolingDesignSupplyAirHumidityRatioInputMethod(
                latent_cooling_design_supply_air_humidity_ratio_input_method)
        if dehumidification_design_supply_air_humidity_ratio is not None:
            sizing.setZoneDehumidificationDesignSupplyAirHumidityRatio(
                dehumidification_design_supply_air_humidity_ratio)
        if cooling_design_supply_air_humidity_ratio_diff is not None:
            sizing.setZoneCoolingDesignSupplyAirHumidityRatioDifference(
                cooling_design_supply_air_humidity_ratio_diff)

        if latent_heating_design_supply_air_humidity_ratio_input_method is not None:
            sizing.setZoneLatentHeatingDesignSupplyAirHumidityRatioInputMethod(
                latent_heating_design_supply_air_humidity_ratio_input_method)
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
        if thermal_zone is not None: space.setThermalZone(thermal_zone)
        if story is not None: space.setBuildingStory(story)

        # Define internal load objects:
        # Lighting:
        lighting_def = LightsDefinition(model)
        lighting_def.setWattsperSpaceFloorArea(lighting_power)
        light = Lights(lighting_def)
        if lighting_schedule is not None: light.setSchedule(lighting_schedule)
        light.setSpace(space)

        # Equipment:
        equipment_def = ElectricEquipmentDefinition(model)
        equipment_def.setWattsperSpaceFloorArea(equipment_power)
        equipment = ElectricEquipment(equipment_def)
        if equipment_schedule is not None: equipment.setSchedule(equipment_schedule)
        equipment.setSpace(space)

        # People:
        people_def = PeopleDefinition(model)
        people_def.setPeopleperSpaceFloorArea(people_density)
        people = People(people_def)
        if occupancy_schedule is not None: people.setNumberofPeopleSchedule(occupancy_schedule)
        if activity_schedule is not None: people.setActivityLevelSchedule(activity_schedule)
        people.setSpace(space)

        # Gas Equipment:
        if gas_power is not None and gas_power != 0:
            gas_def = GasEquipmentDefinition(model)
            gas_def.setWattsperSpaceFloorArea(gas_power)
            gas = GasEquipment(gas_def)
            if gas_schedule is not None: gas.setSchedule(gas_schedule)
            gas.setSpace(space)

        # Space Type:
        space_type = SpaceType(model)
        space_type.setName(program + ":" + name)

        # Outdoor Air:
        outdoor_air = DesignSpecificationOutdoorAir(model)
        outdoor_air.setName(name + "_DSOA")
        outdoor_air.setOutdoorAirMethod("Sum")
        outdoor_air.setOutdoorAirFlowperFloorArea(outdoor_air_per_floor_area)
        outdoor_air.setOutdoorAirFlowperPerson(outdoor_air_per_person)
        if occupancy_schedule is not None: outdoor_air.setOutdoorAirFlowRateFractionSchedule(occupancy_schedule)

        space_type.setDesignSpecificationOutdoorAir(outdoor_air)

        # Infiltration Flow Rate:
        infiltration = SpaceInfiltrationDesignFlowRate(model)
        infiltration.setSpaceType(space_type)
        infiltration.setFlowperExteriorSurfaceArea(0.000226568446)
        if infiltration_schedule is not None: infiltration.setSchedule(infiltration_schedule)

        # Apply space type:
        space.setSpaceType(space_type)

        return space

    @staticmethod
    def space(
            model: openstudio.openstudiomodel.Model,
            name: str,
            program: str,
            thermal_zone: ThermalZone = None,
            story: BuildingStory = None,
            lights: Lights = None,
            people: People = None,
            electric_equipment: ElectricEquipment = None,
            gas_equipment: GasEquipment = None,
            internal_mass: InternalMass = None,
            outdoor_air: DesignSpecificationOutdoorAir = None,
            infiltration:SpaceInfiltrationDesignFlowRate = None):

        space = Space(model)
        space.setName(name)
        if thermal_zone is not None: space.setThermalZone(thermal_zone)
        if story is not None: space.setBuildingStory(story)

        # Space Type:
        space_type = SpaceType(model)
        space_type.setName(program + ":" + name)

        if lights is not None: lights.setSpace(space)
        if people is not None: people.setSpace(space)
        if electric_equipment is not None: electric_equipment.setSpace(space)
        if gas_equipment is not None: gas_equipment.setSpace(space)
        if internal_mass is not None: internal_mass.setSpace(space)
        if outdoor_air is not None:
            space_type.setDesignSpecificationOutdoorAir(outdoor_air)
        if infiltration is not None:
            infiltration.setSpaceType(space_type)

        return space