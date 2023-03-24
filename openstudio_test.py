import math
import openstudio
from openstudio import *
from openstudio.openstudiomodel import Model
from openstudio.openstudioutilitiesgeometry import Point3d, Vector3d, Plane
from Geometry.GeometryTools import GeometryTool
from SiteAndLocation.SiteTools import SiteLocationTool
from SimulationSettings.SimulationSettings import SimulationSettingTool
from OutputData.OutputData import output_variables
from Resources.ExteriorEquipments import ExteriorEquipments
from Resources.ZoneTools import ZoneTool
from Resources.InternalLoad import InternalLoad
from Schedules.Templates.Template import Office, Residential
from Schedules.ScheduleTools import ScheduleTool
from Constructions.ConstructionSets import ConstructionSet
from HVACSystem.PlantLoopComponents import PlantLoopComponent
from HVACSystem.SetpointManagers import SetpointManager
from HVACSystem.AirLoopComponents import AirLoopComponent
from HVACSystem.Template.ASHRAE import ASHRAEBaseline
from HVACSystem.Template.Template import Template
from HVACSystem.ZoneEquipments import ZoneEquipment
from HVACSystem.PerformanceCurves import Curve
from Resources.Helpers import Helper

# vertices = []
path_str = "D:\Projects\OpenStudioDev\Model_350.osm"
newPath_str = "D:\Projects\OpenStudioDev\Model_2.osm"
# newPath_str = "D:\Projects\OpenStudioDev\Model_gbxml.xml"
path = openstudioutilitiescore.toPath(path_str)
newPath = openstudioutilitiescore.toPath(newPath_str)

epw_path_str = "D:\Projects\OpenStudioDev\CHN_Shanghai.Shanghai.583670_IWEC.epw"

ddy_path_str = "D:\Projects\OpenStudioDev\CHN_Shanghai.Shanghai.583670_IWEC.ddy"
ddy_path = openstudioutilitiescore.toPath(ddy_path_str)

# Get the model:
# **************************************************************************************
model = Model.load(path).get()
building = GeometryTool.building(model, "Kunyu's Tower", 34)
stories = GeometryTool.building_story(model, number_of_story=3)

# openstudio.gbxml.GbXMLForwardTranslator().modelToGbXML(model, newPath)

# Weather file:
# **************************************************************************************
SiteLocationTool.set_weather_file(model, epw_path_str)

# Site and design days:
# **************************************************************************************
SiteLocationTool.set_site_and_design_days(model, ddy_path_str)

# Run period:
# **************************************************************************************
SimulationSettingTool.set_run_period(model)
SimulationSettingTool.simulation_controls(model, "FullExterior")

# Output variables:
# **************************************************************************************
output_variables(model, ["Chiller Electricity Energy", "Boiler NaturalGas Energy"])

# Exterior Equipment:
# **************************************************************************************
ExteriorEquipments.exterior_lights(model, design_level=243)
ExteriorEquipments.exterior_fuel(model, design_level=58)

# Space with load:
# **************************************************************************************
office_sch = Office(model)
resid_sch = Residential(model)
space_1 = ZoneTool.space_simplified(
    model,
    name="Kunyu's room 1",
    program="Office",
    lighting_power=0.7,
    equipment_power=1.5,
    people_density=0.5,
    outdoor_air_per_person=0.05,
    outdoor_air_per_floor_area=0.15,
    lighting_schedule=office_sch.lighting(),
    equipment_schedule=office_sch.equipment(),
    occupancy_schedule=office_sch.occupancy(),
    activity_schedule=office_sch.activity_level(),
    infiltration_schedule=office_sch.infiltration())

space_2 = ZoneTool.space_simplified(
    model,
    name="Kunyu's room 2",
    program="Office",
    lighting_power=1.4,
    equipment_power=2.8,
    people_density=0.2,
    outdoor_air_per_person=0.05,
    outdoor_air_per_floor_area=0.15,
    lighting_schedule=resid_sch.lighting(),
    equipment_schedule=resid_sch.equipment(),
    occupancy_schedule=resid_sch.occupancy(),
    activity_schedule=resid_sch.activity_level(),
    infiltration_schedule=resid_sch.infiltration())

# Load Definition:
# **************************************************************************************
InternalLoad.add_lights(model, space_1, lighting_power=3.75, lighting_schedule=office_sch.lighting())
# InternalLoad.add_people(
#     model,
#     space_1,
#     amount=2.3,
#     schedule=office_sch.occupancy(),
#     activity_schedule=office_sch.activity_level(),
#     enable_ashrae55_warning=True,
#     mrt_calc_type="SurfaceWeighted",
#     thermal_comfort_model_type=["AdaptiveASH55", "KSU"])

# Thermal zones:
# **************************************************************************************
thermal_zones = ZoneTool.thermal_zone_from_space(
    model,
    spaces=[space_1, space_2],
    cooling_setpoint_schedules=[office_sch.cooling_setpoint(), resid_sch.cooling_setpoint()],
    heating_setpoint_schedules=[office_sch.heating_setpoint(), resid_sch.heating_setpoint()],
    use_ideal_air_load=False)

# Geometry tool testing:
# **************************************************************************************
cons_set = ConstructionSet(model, "OMG").get()
floor_plan1 = [[7.0, 0.0, 0.0], [10.0, 0.0, 0.0], [10.0, 5.0, 0.0], [7.0, 5.0, 0.0]]
floor_plan2 = [[10.0, 0.0, 0.0], [10.0, 5.0, 0.0], [14.0, 5.0, 0.0], [14.0, 0.0, 0.0]]
floor_plan3 = [[10.0, 0.0, 3.5], [10.0, 5.0, 3.5], [14.0, 5.0, 3.5], [14.0, 0.0, 3.5]]
# srfs1 = GeometryTool.space_from_extrusion(model, floor_plan1, 3.5, space=space_1, construction_set=cons_set,
#                                           building_story=stories[0])
srfs2 = GeometryTool.space_from_extrusion(model, floor_plan2, 3.5, space=space_2, construction_set=cons_set,
                                          building_story=stories[0])
srfs3 = GeometryTool.space_from_extrusion(model, floor_plan3, 3.5, space=space_1, construction_set=cons_set,
                                          building_story=stories[1])
GeometryTool.solve_adjacency(srfs3 + srfs2)

# Plant loop:
# **************************************************************************************
# chiller1 = PlantLoopComponent.chiller_electric(model, name="chiller 1", condenser_type="AirCooled")
# chiller2 = PlantLoopComponent.chiller_electric(model, name="chiller 2", condenser_type="AirCooled")
# chiller3 = PlantLoopComponent.chiller_electric(model, name="chiller 3", condenser_type="AirCooled")
# pump1 = PlantLoopComponent.pump_variable_speed(model, name="pump 1")
# pump2 = PlantLoopComponent.pump_variable_speed(model, name="pump 2")
# pump3 = PlantLoopComponent.pump_variable_speed(model, name="pump 3")
# pump4 = PlantLoopComponent.pump_constant_speed(model, name="pump 4")
# pump5 = PlantLoopComponent.pump_constant_speed(model, name="pump 5")
# pump6 = PlantLoopComponent.pump_constant_speed(model, name="pump 6")
# adiabatic_pipe = PlantLoopComponent.adiabatic_pipe(model)
# items = [[chiller1, pump1, pump4], [chiller2, pump2, pump5], [chiller3, pump3, pump6], [adiabatic_pipe]]
# spm1 = SetpointManager.outdoor_air_reset(model, "Temperature", 13.3, 6.67, 10, 24)
# spm2 = SetpointManager.outdoor_air_reset(model, "Temperature", 13.3, 6.67, 10, 24)
#
# plant_loop = PlantLoopComponent.plant_loop(
#     model,
#     name="Chilled Water Loop HaHaHa",
#     common_pipe_simulation="TwoWayCommonPipe",
#     supply_branches=items,
#     setpoint_manager=spm1,
#     setpoint_manager_secondary=spm2)
#
# PlantLoopComponent.sizing(model, plant_loop, "Cooling")

# Air loop:
# **************************************************************************************
# air_loop = AirLoopComponent.air_loop(model, "My Air Loop", thermal_zones=thermal_zones)
# Template.vav_chiller_boiler(model, thermal_zones=thermal_zones)
terminals = []
for i in range(len(thermal_zones)):
    vrf_terminal = ZoneEquipment.vrf_terminal(model, "Kunyu's VRF Terminal " + str(i+1), thermal_zone=thermal_zones[i])
    terminals.append(vrf_terminal)
vrf_sys = AirLoopComponent.vrf_system(
    model, "Kunyu's VRF", performance_curve_set=Curve.vrf_performance_curve_set_1(model), terminals=terminals)


# ASHRAEBaseline.system_list()
# **************************************************************************************
# model.save(newPath, True)
