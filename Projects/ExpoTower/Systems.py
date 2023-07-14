import openstudio
from HVACSystem.HVACTools import HVACTool
from HVACSystem.AirLoopComponents import AirLoopComponent
from HVACSystem.PlantLoopComponents import PlantLoopComponent
from HVACSystem.SetpointManagers import SetpointManager
from HVACSystem.ZoneEquipments import ZoneEquipment
from HVACSystem.PerformanceCurves import Curve
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

    # Thermal zone sizing:
    # *****************************************************************************************************
    for zone in all_conditioned_zones:
        ZoneTool.sizing(
            model,
            zone["zone"],
            cooling_design_supply_air_temp=14,
            cooling_design_supply_air_temp_diff=12,
            heating_design_supply_air_temp=30,
            heating_design_supply_air_temp_diff=8,
            zone_load_sizing_method=3)

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
    ahu_supply_air_temp = ScheduleTool.schedule_ruleset(model, 2, supply_air_temp, name="AHU_supply_air_temp")

    fan_curve = Curve.fan_curve_set(1)
    pump_curve = Curve.pump_curve_set(1)

    cooling_coils = []
    heating_coils = []
    elevator_lobbies = []
    # Air loops:
    # *****************************************************************************************************
    for i, story in enumerate(sorted_zones.keys()):
        if story == 1:
            for zone_type in sorted_zones[story].keys():
                if zone_type == "ElevatorLobby":
                    elevator_lobbies.extend(sorted_zones[story][zone_type])
                else:
                    cooling_coil = AirLoopComponent.coil_cooling_water(model, design_inlet_water_temp=8)
                    heating_coil = AirLoopComponent.coil_heating_water(model, inlet_water_temp=45, outlet_water_temp=40)
                    supply_fan = AirLoopComponent.fan_variable_speed(
                        model, fan_total_efficiency=0.72, pressure_rise=400, fan_curve_coeff=fan_curve)
                    # supply_fan = AirLoopComponent.fan_constant_speed(model, fan_total_efficiency=0.72,
                    #                                                  pressure_rise=400)

                    if len(sorted_zones[story][zone_type]) > 1:
                        spm = SetpointManager.scheduled(model, 1, schedule=ahu_supply_air_temp)
                    else:
                        spm = SetpointManager.single_zone_cooling(model, supply_air_temp, 30, sorted_zones[story][zone_type][0])

                    air_loop = HVACTool.air_loop_simplified(
                        model, "AHU-1F-" + zone_type,
                        economizer_type=0,
                        heat_recovery_efficiency=0.6,
                        supply_components=[cooling_coil, heating_coil, supply_fan, spm],
                        air_terminal_type=3,
                        thermal_zones=sorted_zones[story][zone_type],
                        availability=ahu_availability,
                        terminal_schedule=always_on)

                    loop = air_loop[0]
                    AirLoopComponent.sizing(model, loop, 1, central_cooling_capacity_control_method=4)

                    cooling_coils.extend(air_loop[1])
                    heating_coils.extend(air_loop[2])

        elif 2 <= story <= 18:
            zone_by_ahu = {"1W": [], "1N": [], "2W": [], "2N": [], "3W": [], "3N": [], "4W": [], "4N": []}
            zone_name_by_ahu = {"1W": [], "1N": [], "2W": [], "2N": [], "3W": [], "3N": [], "4W": [], "4N": []}
            for zone_type in sorted_zones[story].keys():
                if zone_type == "ElevatorLobby":
                    elevator_lobbies.extend(sorted_zones[story][zone_type])
                else:
                    suffix = zone_type.split("_")[1]
                    match suffix:
                        case "1W":
                            zone_by_ahu["1W"].extend(sorted_zones[story][zone_type])
                            zone_name_by_ahu["1W"].extend(zone.nameString() for zone in sorted_zones[story][zone_type])
                        case "1N":
                            zone_by_ahu["1N"].extend(sorted_zones[story][zone_type])
                            zone_name_by_ahu["1N"].extend(zone.nameString() for zone in sorted_zones[story][zone_type])
                        case "2W":
                            zone_by_ahu["2W"].extend(sorted_zones[story][zone_type])
                            zone_name_by_ahu["2W"].extend(zone.nameString() for zone in sorted_zones[story][zone_type])
                        case "2N":
                            zone_by_ahu["2N"].extend(sorted_zones[story][zone_type])
                            zone_name_by_ahu["2N"].extend(zone.nameString() for zone in sorted_zones[story][zone_type])
                        case "3W":
                            zone_by_ahu["3W"].extend(sorted_zones[story][zone_type])
                            zone_name_by_ahu["3W"].extend(zone.nameString() for zone in sorted_zones[story][zone_type])
                        case "3N":
                            zone_by_ahu["3N"].extend(sorted_zones[story][zone_type])
                            zone_name_by_ahu["3N"].extend(zone.nameString() for zone in sorted_zones[story][zone_type])
                        case "4W":
                            zone_by_ahu["4W"].extend(sorted_zones[story][zone_type])
                            zone_name_by_ahu["4W"].extend(zone.nameString() for zone in sorted_zones[story][zone_type])
                        case "4N":
                            zone_by_ahu["4N"].extend(sorted_zones[story][zone_type])
                            zone_name_by_ahu["4N"].extend(zone.nameString() for zone in sorted_zones[story][zone_type])

            # print(zone_name_by_ahu)
            for key in zone_by_ahu.keys():
                if len(zone_by_ahu[key]) != 0:
                    cooling_coil = AirLoopComponent.coil_cooling_water(model, design_inlet_water_temp=8)
                    heating_coil = AirLoopComponent.coil_heating_water(model, inlet_water_temp=45, outlet_water_temp=40)
                    supply_fan = AirLoopComponent.fan_variable_speed(
                        model, fan_total_efficiency=0.72, pressure_rise=500, fan_curve_coeff=fan_curve)
                    # supply_fan = AirLoopComponent.fan_constant_speed(
                    #     model, fan_total_efficiency=0.72, pressure_rise=500)

                    if len(zone_by_ahu[key]) > 1:
                        spm = SetpointManager.scheduled(model, 1, schedule=ahu_supply_air_temp)
                    else:
                        spm = SetpointManager.single_zone_cooling(model, supply_air_temp, 30, zone_by_ahu[key][0])

                    air_loop = HVACTool.air_loop_simplified(
                        model, "AHU-{}F-{}".format(story, key),
                        economizer_type=1,
                        heat_recovery_efficiency=0.6,
                        supply_components=[cooling_coil, heating_coil, supply_fan, spm],
                        air_terminal_type=3,
                        thermal_zones=zone_by_ahu[key],
                        availability=ahu_availability,
                        terminal_schedule=always_on)

                    loop = air_loop[0]
                    AirLoopComponent.sizing(model, loop, 1, central_cooling_capacity_control_method=4)

                    cooling_coils.extend(air_loop[1])
                    heating_coils.extend(air_loop[2])

                else:
                    pass
        else:
            pass

    # Plant loops:
    # *****************************************************************************************************
    heatpump_cooling_1 = PlantLoopComponent.heat_pump_plant_cooling(model, 1, 3200000, cop=7.5)
    heatpump_heating_1 = PlantLoopComponent.heat_pump_plant_heating(model, 1, 2800000, cop=4.5)

    heatpump_cooling_1.setCompanionHeatingHeatPump(heatpump_heating_1)
    heatpump_heating_1.setCompanionCoolingHeatPump(heatpump_cooling_1)

    district_cooling = PlantLoopComponent.district_cooling(model)
    # district_heating = PlantLoopComponent.district_heating(model)

    pump_cooling_1 = PlantLoopComponent.pump_variable_speed(
        model, rated_head=Helper.mh2o_to_pa(34), rated_flow_rate=0.2, control_type=2, pump_curve_coeff=pump_curve)
    pump_cooling_2 = PlantLoopComponent.pump_variable_speed(
        model, rated_head=Helper.mh2o_to_pa(34), rated_flow_rate=0.2, control_type=2, pump_curve_coeff=pump_curve)
    pump_heating_1 = PlantLoopComponent.pump_variable_speed(
        model, rated_head=Helper.mh2o_to_pa(26), rated_flow_rate=0.06, control_type=2, pump_curve_coeff=pump_curve)
    # pump_heating_2 = PlantLoopComponent.pump_variable_speed(
    #     model, rated_head=Helper.mh2o_to_pa(26), pump_curve_coeff=pump_curve)

    chilled_water_loop = HVACTool.plant_loop(
        model, "Chilled Water Loop", 1,
        load_distribution_scheme=2,
        common_pipe_simulation=1,
        setpoint_manager=SetpointManager.scheduled(model, 1, 7, name="Chilled_Water_Supply_Temp"),
        supply_branches=[[pump_cooling_1, heatpump_cooling_1], [pump_cooling_2, district_cooling]],
        demand_branches=cooling_coils,
        availability=plant_availability)

    PlantLoopComponent.sizing(model, chilled_water_loop, 1, 8, 5)

    hot_water_loop = HVACTool.plant_loop(
        model, "Hot Water Loop", 1,
        load_distribution_scheme=2,
        common_pipe_simulation=1,
        setpoint_manager=SetpointManager.scheduled(model, 1, 45, name="Hot_Water_Supply_Temp"),
        supply_branches=[pump_heating_1, heatpump_heating_1],
        demand_branches=heating_coils,
        availability=plant_availability)

    PlantLoopComponent.sizing(model, hot_water_loop, 2, 45, 5)

    # Zone Equipments (FCUs for elevator lobby):
    # *****************************************************************************************************
    if len(elevator_lobbies) != 0:
        for ele_lobby in elevator_lobbies:

            cooling_coil = AirLoopComponent.coil_cooling_water(model, design_inlet_water_temp=8)
            heating_coil = AirLoopComponent.coil_heating_water(model, inlet_water_temp=45, outlet_water_temp=40)
            fan = AirLoopComponent.fan_variable_speed(
                model, fan_total_efficiency=0.72, pressure_rise=50, fan_curve_coeff=fan_curve)

            ZoneEquipment.fan_coil_unit_detailed(
                model,
                fan,
                cooling_coil,
                heating_coil,
                schedule=always_on,
                thermal_zone=ele_lobby,
                capacity_control_method=1,
                chilled_water_loop=chilled_water_loop,
                hot_water_loop=hot_water_loop)

            # ZoneEquipment.fan_coil_unit(
            #     model,
            #     schedule=always_on,
            #     thermal_zone=ele_lobby,
            #     capacity_control_method=1,
            #     fan_pressure_rise=50,
            #     chilled_water_loop=chilled_water_loop,
            #     hot_water_loop=hot_water_loop)

    # Notification:
    # *****************************************************************************************************
    print("Step 5-5: HVAC system All Set.")
