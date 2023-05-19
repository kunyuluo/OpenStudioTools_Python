import openstudio
from HVACSystem.HVACTools import HVACTool
from HVACSystem.AirLoopComponents import AirLoopComponent
from HVACSystem.PlantLoopComponents import PlantLoopComponent
from HVACSystem.SetpointManagers import SetpointManager
from Resources.ZoneTools import ZoneTool
from Resources.Helpers import Helper


def hvac_system(model: openstudio.openstudiomodel.Model, thermal_zones):

    """
    -thermal_zones: Use output from "geometry_from_json" here
    """

    # Sort the thermal zones:
    all_zones = ZoneTool.get_thermal_zone(thermal_zones)
    sorted_zones = ZoneTool.thermal_zone_by_floor(thermal_zones, True)

    cooling_coil = AirLoopComponent.coil_cooling_water(model)
    spm_1 = SetpointManager.scheduled(model, 1, 0.008)
    heating_coil = AirLoopComponent.coil_heating_electric(model)
    supply_fan = AirLoopComponent.fan_variable_speed(model, pressure_rise=Helper.mh2o_to_pa(4.5))
    spm_2 = SetpointManager.scheduled(model, 1, Helper.f_to_c(55))

    air_loop = HVACTool.air_loop_simplified(
        model, "AHU-1-1", economizer_type=1, heat_recovery_efficiency=0.6,
        supply_components=[cooling_coil, spm_1, heating_coil, supply_fan, spm_2], thermal_zones=all_zones)

    loop = air_loop[0]

    heatpump = openstudio.openstudiomodel.HeatPumpPlantLoopEIRCooling(model)

    chilled_water_loop = HVACTool.plant_loop(
        model, "Chilled Water Loop", 1,
        common_pipe_simulation=1,
        setpoint_manager=SetpointManager.outdoor_air_reset(model, ashrae_default=2),
        supply_branches=[heatpump])

    PlantLoopComponent.sizing(model, chilled_water_loop, 1)
