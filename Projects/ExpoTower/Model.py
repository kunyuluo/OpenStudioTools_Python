from Constructions.ConstructionTools import ConstructionTool
from Resources.Models import create_model
from Resources.InternalLoad import InternalLoad
from RhinoGeometry.RhinoParse import load_rhino_model
from Geometry.GeometryTools import GeometryTool
from Resources.ZoneTools import ZoneTool
from Resources.Helpers import Helper
from SimulationSettings.SimulationSettings import SimulationSettingTool
from Projects.ExpoTower.Systems import hvac_system
from Projects.ExpoTower.Schedule import add_schedules
from OutputData.OutputData import output_variables

# Project Info:
# **************************************************************************************
project_name = "ExpoTower"
building_name = "ExpoTower"
rhino_model_path = "D:\\Projects\\OpenStudioDev\\RhinoGeometry\\ExpoTower_Geo_TypicalFlr.3dm"

# Weather file:
# **************************************************************************************
epw_path_str = "D:\\Projects\\OpenStudioDev\\CHN_Shanghai.Shanghai.583670_IWEC.epw"
ddy_path_str = "D:\\Projects\\OpenStudioDev\\CHN_Shanghai.Shanghai.583670_IWEC.ddy"
path_str = "D:\\Projects\\OpenStudioDev\\ExpoTower_TypicalFlr.osm"
#
# # Create a new openstudio model
# # **************************************************************************************
model_file = create_model(epw_path_str, ddy_path_str, path_str, "Expo Tower", north_axis=-45)
model = model_file[0]
path = model_file[1]

# Construction set:
# **************************************************************************************
cons_set_1 = ConstructionTool.construction_set_simple(
    model, "1-4F Construction Set", False, 0.58, 0.43, 0.55, 2.2, 0.45, 0.6, 0.57, 0.43, 0.57, 0.43, 0.55)

cons_set_5 = ConstructionTool.construction_set_simple(
    model, "5F Construction Set", False, 0.57, 0.43, 0.55, 2.14, 0.36, 0.6, 0.57, 0.43, 0.57, 0.43, 0.55)

glazing_east_5F = ConstructionTool.simple_glazing_cons(model, "Glazing_East_5F", 2.14, 0.36, 0.6)
glazing_west_5F = ConstructionTool.simple_glazing_cons(model, "Glazing_West_5F", 1.93, 0.33, 0.6)
glazing_north_5F = ConstructionTool.simple_glazing_cons(model, "Glazing_North_5F", 2.15, 0.36, 0.6)
glazing_south_5F = ConstructionTool.simple_glazing_cons(model, "Glazing_South_5F", 1.93, 0.32, 0.6)

ext_wall_east = ConstructionTool.opaque_no_mass_cons(model, "East R-15 Wall", Helper.r_ip_to_si(15))
ext_wall_south = ConstructionTool.opaque_no_mass_cons(model, "South R-19 Wall", Helper.r_ip_to_si(19))

internal_mass_cons = ConstructionTool.opaque_cons(model, "Std Wood 6inch", 0.15, 0.12, 540, 1210, 3)

# Internal Load:
# **************************************************************************************
load_and_space = InternalLoad.internal_load_from_file("D:\\Projects\\OpenStudioDev\\LoadInputs.xlsx", "ExpoTower")
load = load_and_space[0]
space_list = load_and_space[1]

# Schedules:
# **************************************************************************************
schedule_sets = add_schedules(model, space_list)

# Load geometry from Rhino:
# **************************************************************************************
file_path = load_rhino_model(rhino_model_path, project_name, building_name)
geometries = GeometryTool.geometry_from_json(model, file_path, load, cons_set_5, schedule_sets, internal_mass_cons)

# Get all thermal zones for HVAC arrangement:
# **************************************************************************************
thermal_zones = geometries[0]

# Get all exterior wall surfaces for construction assignment:
# **************************************************************************************
ext_walls = geometries[1]
ZoneTool.construction_by_orientation(
    ext_walls, construction_east=ext_wall_east, construction_south=ext_wall_south)

# Get all fenestration surfaces for construction assignment:
# **************************************************************************************
windows = geometries[2]
ZoneTool.construction_by_orientation(
    windows, glazing_east_5F, glazing_west_5F, glazing_north_5F, glazing_south_5F)

# Build HVAC system:
# **************************************************************************************
hvac_system(model, thermal_zones)

# Simulation settings:
# **************************************************************************************
SimulationSettingTool.set_timestep(model, 1)
SimulationSettingTool.heat_balance_algorithm(model, 500)

# Set output variables if any:
# **************************************************************************************
output_variables(model, ["Heating Coil Heating Energy"])

# Save the model to the pre-defined path:
# **************************************************************************************
model.save(path, True)
print("Model is Ready!")
