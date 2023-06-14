import openstudio
from HVACSystem.HVACTools import HVACTool
from HVACSystem.AirLoopComponents import AirLoopComponent
from HVACSystem.PlantLoopComponents import PlantLoopComponent
from HVACSystem.SetpointManagers import SetpointManager
from HVACSystem.ZoneEquipments import ZoneEquipment
from Schedules.ScheduleTools import ScheduleTool
from Resources.ZoneTools import ZoneTool
from Resources.Helpers import Helper


def hvac_system(model: openstudio.openstudiomodel.Model, thermal_zones):

    """
    -thermal_zones: Use output from "geometry_from_json" here
    """

    # Sort the thermal zones:
    # *****************************************************************************************************
    all_conditioned_zones = ZoneTool.thermal_zone_by_conditioned(thermal_zones)[0]
    sorted_zones = ZoneTool.thermal_zone_by_floor(all_conditioned_zones, True)

    # Availability Schedule:
    # *****************************************************************************************************
    plant_availability = ScheduleTool.custom_annual_schedule(
        model, 1,
        [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
        name="Plant_Availability")

    ahu_availability = ScheduleTool.custom_annual_schedule(
        model, 1,
        [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
        name="AHU_Availability")

    always_on = ScheduleTool.always_on(model)

    # Parameters:
    # *****************************************************************************************************
    supply_air_temp = 14

    cooling_coils = []
    heating_coils = []
    elevator_lobbies = []
    # Air loops:
    # *****************************************************************************************************
    for i, story in enumerate(sorted_zones.keys()):
        if story == 100:
            for zone_type in sorted_zones[story].keys():
                if zone_type == "ElevatorLobby":
                    elevator_lobbies.extend(sorted_zones[story][zone_type])
                else:
                    cooling_coil = AirLoopComponent.coil_cooling_water(model)
                    heating_coil = AirLoopComponent.coil_heating_electric(model)
                    supply_fan = AirLoopComponent.fan_variable_speed(model, pressure_rise=Helper.mh2o_to_pa(4.5))
                    spm_2 = SetpointManager.scheduled(model, 1, supply_air_temp, name="AHU_Supply_Air_Temp")

                    air_loop = HVACTool.air_loop_simplified(
                        model, "AHU-1F-" + zone_type,
                        economizer_type=0,
                        heat_recovery_efficiency=0.6,
                        supply_components=[cooling_coil, heating_coil, supply_fan, spm_2],
                        air_terminal_type=3,
                        thermal_zones=sorted_zones[story][zone_type],
                        availability=ahu_availability)

                    loop = air_loop[0]
                    AirLoopComponent.sizing(model, loop, 1)

                    cooling_coils.extend(air_loop[1])
                    heating_coils.extend(air_loop[2])

        elif 1 <= story <= 18:
            zone_by_ahu = {"1W": [], "1N": [], "2W": [], "2N": [], "3W": [], "3N": [], "4W": [], "4N": []}
            for zone_type in sorted_zones[story].keys():
                if zone_type == "ElevatorLobby":
                    elevator_lobbies.extend(sorted_zones[story][zone_type])
                else:
                    suffix = zone_type.split("_")[1]
                    match suffix:
                        case "1W":
                            zone_by_ahu["1W"].extend(sorted_zones[story][zone_type])
                        case "1N":
                            zone_by_ahu["1N"].extend(sorted_zones[story][zone_type])
                        case "2W":
                            zone_by_ahu["2W"].extend(sorted_zones[story][zone_type])
                        case "2N":
                            zone_by_ahu["2N"].extend(sorted_zones[story][zone_type])
                        case "3W":
                            zone_by_ahu["3W"].extend(sorted_zones[story][zone_type])
                        case "3N":
                            zone_by_ahu["3N"].extend(sorted_zones[story][zone_type])
                        case "4W":
                            zone_by_ahu["4W"].extend(sorted_zones[story][zone_type])
                        case "4N":
                            zone_by_ahu["4N"].extend(sorted_zones[story][zone_type])

            for key in zone_by_ahu.keys():
                cooling_coil = AirLoopComponent.coil_cooling_water(model)
                heating_coil = AirLoopComponent.coil_heating_electric(model)
                reheat_coil = AirLoopComponent.coil_heating_electric(model)
                supply_fan = AirLoopComponent.fan_variable_speed(model, pressure_rise=Helper.mh2o_to_pa(4.5))
                # spm_2 = SetpointManager.scheduled(model, 1, supply_air_temp, name="AHU_Supply_Air_Temp")
                # spm_2 = SetpointManager.warmest(model, 14, 12)

                # for zone in zone_by_ahu[key]:
                #     pass

                unitary = AirLoopComponent.unitary_system(
                    model, cooling_coil, heating_coil, reheat_coil, supply_fan,
                    dehumidification_control_type=3, latent_load_control=3, control_zone=zone_by_ahu[key][0],
                    availability_schedule=ahu_availability, fan_placement=2, supply_fan_schedule=always_on,
                    supply_air_flow_rate_method_cooling=1, supply_air_flow_rate_method_heating=1,
                    supply_air_flow_rate_method_none=3, fraction_clg_supply_air_flow_rate_none=0.05)

                air_loop = HVACTool.air_loop_simplified(
                    model, "AHU-{}F-{}".format(story, key),
                    economizer_type=0,
                    heat_recovery_efficiency=0.6,
                    supply_components=[unitary],
                    air_terminal_type=3,
                    thermal_zones=zone_by_ahu[key],
                    availability=ahu_availability)

                loop = air_loop[0]
                AirLoopComponent.sizing(model, loop, 1)

                cooling_coils.extend(cooling_coil)
                cooling_coils.extend(air_loop[1])
                # heating_coils.extend(air_loop[2])

        else:
            pass

    # Plant loops:
    # *****************************************************************************************************
    heatpump_cooling = PlantLoopComponent.heat_pump_plant_cooling(model, 1, 3000, 7.5)
    heatpump_heating = PlantLoopComponent.heat_pump_plant_heating(model, 1, 3000, 4.5)

    chiller = PlantLoopComponent.chiller_electric(model, condenser_type=1, capacity=8000, cop=7.5)
    boiler = PlantLoopComponent.boiler_hot_water(model, fuel_type=2, nominal_capacity=8000)

    heatpump_cooling.setCompanionHeatingHeatPump(heatpump_heating)
    heatpump_heating.setCompanionCoolingHeatPump(heatpump_cooling)

    district_cooling = PlantLoopComponent.district_cooling(model)
    district_heating = PlantLoopComponent.district_heating(model)

    pump_cooling_1 = PlantLoopComponent.pump_variable_speed(model)
    pump_cooling_2 = PlantLoopComponent.pump_variable_speed(model)
    pump_heating_1 = PlantLoopComponent.pump_variable_speed(model)
    pump_heating_2 = PlantLoopComponent.pump_variable_speed(model)

    chilled_water_loop = HVACTool.plant_loop(
        model, "Chilled Water Loop", 1,
        load_distribution_scheme=2,
        common_pipe_simulation=1,
        setpoint_manager=SetpointManager.scheduled(model, 1, 7, name="Chilled_Water_Supply_Temp"),
        supply_branches=[[pump_cooling_1, chiller], [pump_cooling_2, district_cooling]],
        demand_branches=cooling_coils,
        availability=plant_availability)

    PlantLoopComponent.sizing(model, chilled_water_loop, 1)

    hot_water_loop = HVACTool.plant_loop(
        model, "Hot Water Loop", 1,
        load_distribution_scheme=2,
        common_pipe_simulation=1,
        setpoint_manager=SetpointManager.scheduled(model, 1, 45, name="Hot_Water_Supply_Temp"),
        supply_branches=[[pump_heating_1, boiler], [pump_heating_2, district_heating]],
        demand_branches=heating_coils,
        availability=plant_availability)

    PlantLoopComponent.sizing(model, hot_water_loop, 1)

    # Zone Equipments (FCUs for elevator lobby):
    # *****************************************************************************************************
    if len(elevator_lobbies) != 0:
        for ele_lobby in elevator_lobbies:
            fcu = ZoneEquipment.fan_coil_unit(
                model,
                thermal_zone=ele_lobby,
                fan_pressure_rise=250,
                chilled_water_loop=chilled_water_loop,
                hot_water_loop=hot_water_loop)
