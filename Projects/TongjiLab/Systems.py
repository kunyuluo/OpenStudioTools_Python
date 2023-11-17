import openstudio
from HVACSystem.HVACTools import HVACTool
from HVACSystem.AirLoopComponents import AirLoopComponent
from HVACSystem.PlantLoopComponents import PlantLoopComponent
from HVACSystem.SetpointManagers import SetpointManager
from HVACSystem.PerformanceCurves import Curve
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
        [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        name="Plant_Availability")

    ahu_availability = ScheduleTool.custom_annual_schedule(
        model, 1,
        [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        name="AHU_Availability")

    always_on = ScheduleTool.always_on(model)

    # Parameters:
    # *****************************************************************************************************
    supply_air_temp = 18
    supply_clg_water_temp = 7
    return_clg_water_temp = 12
    supply_htg_water_temp = 45
    return_htg_water_temp = 40
    design_flow_rate = 1000
    clg_delta_t = return_clg_water_temp - supply_clg_water_temp
    htg_delta_t = supply_htg_water_temp - return_htg_water_temp

    ahu_supply_air_temp = ScheduleTool.schedule_ruleset(model, 2, supply_air_temp, name="AHU_supply_air_temp")
    ahu_supply_air_humid = ScheduleTool.schedule_ruleset(model, 1, 0.0035, name="AHU_supply_air_humid")
    min_air_fraction_schedule = ScheduleTool.custom_annual_schedule(
        model, 1,
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        name="Lab_Occupancy")

    fan_curve = Curve.fan_curve_set(1)
    pump_curve = Curve.pump_curve_set(1)

    cooling_coils = []
    heating_coils = []

    # Air loops:
    # *****************************************************************************************************
    thermal_zones = [zone['zone'] for zone in all_conditioned_zones]

    cooling_coil = AirLoopComponent.coil_cooling_water(model, design_inlet_water_temp=supply_clg_water_temp)

    heating_coil = AirLoopComponent.coil_heating_water(
        model, inlet_water_temp=supply_htg_water_temp, outlet_water_temp=return_htg_water_temp)

    reheat_coil = AirLoopComponent.coil_heating_electric(model)

    humidifier = AirLoopComponent.humidifier_electric(model, power=2300)

    supply_fan = AirLoopComponent.fan_variable_speed(
        model, fan_total_efficiency=0.72, pressure_rise=440, max_flow_rate=design_flow_rate / 3600, fan_curve_coeff=fan_curve)

    # if len(thermal_zones) > 1:
    #     spm = SetpointManager.scheduled(model, 1, schedule=ahu_supply_air_temp)
    # else:
    #     spm = SetpointManager.single_zone_cooling(model, supply_air_temp, 30, thermal_zones[0])

    spm = SetpointManager.scheduled(model, 1, schedule=ahu_supply_air_temp)
    spm_2 = SetpointManager.scheduled(model, 6, schedule=ahu_supply_air_humid)

    air_loop = HVACTool.air_loop_simplified(
        model, "DOAS-Lab",
        economizer_type=0,
        supply_components=[supply_fan, cooling_coil, heating_coil, reheat_coil, humidifier, spm, spm_2],
        air_terminal_type=3,
        air_terminal_for_doas=True,
        air_terminal_for_dcv=True,
        thermal_zones=thermal_zones,
        availability=ahu_availability,
        terminal_schedule=always_on,
        min_air_fraction_schedule=min_air_fraction_schedule)

    loop = air_loop[0]
    AirLoopComponent.sizing(model, loop, 3, all_outdoor_air_cooling=True, all_outdoor_air_heating=True)

    cooling_coils.extend(air_loop[1])
    heating_coils.extend(air_loop[2])

    # Plant loops:
    # *****************************************************************************************************
    district_cooling = PlantLoopComponent.district_cooling(model)
    district_heating = PlantLoopComponent.district_heating(model)

    pump_cooling = PlantLoopComponent.pump_variable_speed(model, control_type=2, pump_curve_coeff=pump_curve)
    pump_heating = PlantLoopComponent.pump_variable_speed(model, control_type=2, pump_curve_coeff=pump_curve)

    chilled_water_loop = HVACTool.plant_loop(
        model, "Chilled Water Loop", 1,
        load_distribution_scheme=1,
        common_pipe_simulation=1,
        setpoint_manager=SetpointManager.scheduled(model, 1, supply_clg_water_temp, name="Chilled_Water_Supply_Temp"),
        supply_branches=[pump_cooling, district_cooling],
        demand_branches=cooling_coils,
        availability=plant_availability)

    PlantLoopComponent.sizing(model, chilled_water_loop, 1, supply_clg_water_temp, clg_delta_t)

    hot_water_loop = HVACTool.plant_loop(
        model, "Hot Water Loop", 1,
        load_distribution_scheme=1,
        common_pipe_simulation=1,
        setpoint_manager=SetpointManager.scheduled(model, 1, supply_htg_water_temp, name="Hot_Water_Supply_Temp"),
        supply_branches=[pump_heating, district_heating],
        demand_branches=heating_coils,
        availability=plant_availability)

    PlantLoopComponent.sizing(model, hot_water_loop, 2, supply_htg_water_temp, htg_delta_t)

    # Zone Equipments (FCU):
    # *****************************************************************************************************
    for zone in thermal_zones:

        cooling_coil = AirLoopComponent.coil_cooling_water(model, design_inlet_water_temp=7)
        heating_coil = AirLoopComponent.coil_heating_water(model, inlet_water_temp=45, outlet_water_temp=40)
        fan = AirLoopComponent.fan_variable_speed(
            model, fan_total_efficiency=0.72, pressure_rise=50, fan_curve_coeff=fan_curve)

        ZoneEquipment.fan_coil_unit_detailed(
            model,
            fan,
            cooling_coil,
            heating_coil,
            schedule=always_on,
            thermal_zone=zone,
            capacity_control_method=1,
            chilled_water_loop=chilled_water_loop,
            hot_water_loop=hot_water_loop)

    # Notification:
    # *****************************************************************************************************
    print("Step 5-5: HVAC system All Set.")
