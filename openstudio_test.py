from openstudio import *
from openstudio.openstudiomodel import Model
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
from HVACSystem.AirTerminals import AirTerminal
from HVACSystem.Template.ASHRAE import ASHRAEBaseline
from HVACSystem.Template.Template import Template
from HVACSystem.ZoneEquipments import ZoneEquipment
from HVACSystem.PerformanceCurves import Curve
from HVACSystem.HVACTools import HVACTool
from Resources.Helpers import Helper
from RhinoGeometry.RhinoParse import load_rhino_model, modify_rhino_unit

# vertices = []
path_str = "D:\\Projects\\OpenStudioDev\\Model_350.osm"
newPath_str = "D:\\Projects\\OpenStudioDev\\Model_2.osm"
# newPath_str = "D:\Projects\OpenStudioDev\Model_gbxml.xml"
path = openstudioutilitiescore.toPath(path_str)
newPath = openstudioutilitiescore.toPath(newPath_str)

epw_path_str = "D:\\Projects\\OpenStudioDev\\CHN_Shanghai.Shanghai.583670_IWEC.epw"

ddy_path_str = "D:\\Projects\\OpenStudioDev\\CHN_Shanghai.Shanghai.583670_IWEC.ddy"
ddy_path = openstudioutilitiescore.toPath(ddy_path_str)

# Get the model:
# **************************************************************************************
model = Model.load(path).get()
building = GeometryTool.building(model, "Kunyu's Tower", 34)

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
ExteriorEquipments.exterior_lights(model, design_level=24)

# Space with load:
# **************************************************************************************
office_sch = Office(model)
# resid_sch = Residential(model)

# load = InternalLoad.internal_load_input_json(
#     ["Office", "Conference", "Corridor"],
#     [0.8, 1.3, 0.6],
#     [1.2, 1.8, 0.5],
#     [0.1, 0.3, 0.05],
#     [200, 200, 200],
#     [0.15, 0.15, 0.15],
#     [0.2, 0.2, 0.2],
#     [3, 1, 3])
#
# file_path = load_rhino_model("D:\\Projects\\OpenStudioDev\\RhinoGeometry\\geometry_test.3dm", "Kunyu_House")
# thermal_zones = GeometryTool.geometry_from_json(model, file_path, internal_load=load)
# sorted_zones = ZoneTool.thermal_zone_by_floor(thermal_zones, True)
#
# print(len(sorted_zones[2]["Office"]))

# Air loop:
# **************************************************************************************
# terminals = []
# for i in range(len(thermal_zones)):
#     vrf_terminal = ZoneEquipment.vrf_terminal(
#     model, "Kunyu VRF Terminal " + str(i+1), thermal_zone=thermal_zones[i])
#     terminals.append(vrf_terminal)
# vrf_sys = Template.vrf_system(
#     model, "Kunyu VRF", performance_curve_set=Curve.vrf_performance_curve_set_1(model), terminals=terminals)

# variable_1 = [5.0,5.56,6.11,6.67,7.22,7.78,8.33,8.89,9.44,10.0]
# Helper.visualize_curve(
#     Curve.biquadratic(model,0.258,0.0389,-0.00022,0.0469,-0.00094,-0.00034),
#     normalize=False, variable_1=variable_1, variable_2=29.44,
#     reference_curve=Curve.biquadratic(model,1.35608,0.04875,-0.00089,-0.01453,-0.00029,-0.00004))

# Helper.visualize_curve_numeric("cubic", Curve.pump_curve_set(0), reference_curve=Curve.pump_curve_set(1))

# Template.vav_chiller_boiler(model, thermal_zones, number_of_chiller=2, chiller_cop=6.8, chiller_condenser_type=2)
#
# shw_loop = HVACTool.service_hot_water_loop(
#     model, "Kunyu SHW Loop", 3, 0.98,
#     water_use_connections=PlantLoopComponent.water_use_connection(model, InternalLoad.water_use_equipment(model)))
# ASHRAEBaseline.system_list()
# **************************************************************************************
# model.save(newPath, True)
