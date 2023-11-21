from Constructions.ConstructionTools import ConstructionTool
from Resources.Models import create_model
from Resources.InternalLoad import InternalLoad
from RhinoGeometry.RhinoParse import load_rhino_model
from Geometry.GeometryTools import GeometryTool
from Resources.ZoneTools import ZoneTool
from HVACSystem.HVACTools import HVACTool
from SimulationSettings.SimulationSettings import SimulationSettingTool
from Projects.TongjiLab.Schedule import add_schedules
from OutputData.OutputData import output_variables
from Projects.TongjiLab.Systems import hvac_system

# Project Info:
# **************************************************************************************
project_name = "TongjiLab"
building_name = "TongjiLab"
rhino_model_path = "D:\\Projects\\OpenStudioDev\\RhinoGeometry\\Lab.3dm"

# Weather file:
# **************************************************************************************
epw_path_str = "D:\\Projects\\OpenStudioDev\\CHN_Shanghai.Shanghai.583670_IWEC.epw"
path_str = "D:\\Projects\\OpenStudioDev\\Tongji_Lab.osm"
#
# # Create a new openstudio model
# # **************************************************************************************
model_file = create_model(epw_path_str, path_str, "Tongji_Lab", north_axis=40)
model = model_file[0]
path = model_file[1]

# Construction set:
# **************************************************************************************
cons_set_1 = ConstructionTool.construction_set_simple(
    model, "Construction Set", False, 0.72, 0.43, 0.55, 3.3, 0.45, 0.6, 1.66, 0.43, 0.57, 0.43, 0.55)

internal_mass_cons = ConstructionTool.opaque_cons(model, "Std Wood 6inch", 0.15, 0.12, 540, 1210, 3)

# Internal Load:
# **************************************************************************************
load_and_space = InternalLoad.internal_load_from_file("D:\\Projects\\OpenStudioDev\\LoadInputs.xlsx", "Tongji_Lab")
load = load_and_space[0]
space_list = load_and_space[1]

# Schedules:
# **************************************************************************************
schedule_sets = add_schedules(model, space_list)

# Load geometry from Rhino:
# **************************************************************************************
file_path = load_rhino_model(rhino_model_path, project_name, building_name)
geometries = GeometryTool.geometry_from_json(model, file_path, load, cons_set_1, schedule_sets, internal_mass_cons)

# Get all thermal zones for HVAC arrangement:
# **************************************************************************************
thermal_zones = geometries[0]

# Build HVAC system:
# **************************************************************************************
# HVACTool.ideal_air_load(ZoneTool.thermal_zone_by_conditioned(thermal_zones)[0])
hvac_system(model, thermal_zones)

# Simulation settings:
# **************************************************************************************
SimulationSettingTool.set_run_period(model, 1, 1, 12, 31)
SimulationSettingTool.set_timestep(model, 1)
SimulationSettingTool.heat_balance_algorithm(model, 500)

# Set output variables if any:
# **************************************************************************************
# output_variables(model, ["Zone Ideal Loads Supply Air Total Cooling Energy", "Zone Ideal Loads Supply Air Total Heating Energy"])

# Save the model to the pre-defined path:
# **************************************************************************************
model.save(path, True)
print("Model is Ready!")

