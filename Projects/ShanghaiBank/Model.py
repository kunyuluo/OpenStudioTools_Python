from Constructions.ConstructionTools import ConstructionTool
from Resources.Models import create_model
from Resources.InternalLoad import InternalLoad
from RhinoGeometry.RhinoParse import load_rhino_model
from Geometry.GeometryTools import GeometryTool
from Resources.ZoneTools import ZoneTool
from SimulationSettings.SimulationSettings import SimulationSettingTool
from Projects.ShanghaiBank.Schedule import add_schedules

# Project Info:
# **************************************************************************************
project_name = "ShanghaiBank"
building_name = "ShanghaiBank"
rhino_model_path = "D:\\Projects\\OpenStudioDev\\RhinoGeometry\\ShanghaiBank_Energy.3dm"

# Weather file:
# **************************************************************************************
epw_path_str = "D:\\Projects\\OpenStudioDev\\CHN_Shanghai.Shanghai.583670_IWEC.epw"
path_str = "D:\\Projects\\OpenStudioDev\\SHBankTower_BC.osm"
#
# # Create a new openstudio model
# # **************************************************************************************
model_file = create_model(epw_path_str, path_str, "SH Bank Tower", north_axis=18.7)
model = model_file[0]
path = model_file[1]

# Construction set:
# **************************************************************************************
cons_set = ConstructionTool.construction_set_simple(
    model, "Construction Set DC", False, 0.53, 0.44, 0.67, 2.2, 0.3, 0.6, 0.57, 0.43, 0.57, 0.43, 0.55)

cons_set_b = ConstructionTool.construction_set_simple(
    model, "Construction Set BC", False, 0.8, 0.5, 0.8, 2.2, 0.3, 0.6, 0.57, 0.43, 0.57, 0.43, 0.55)

glazing_east = ConstructionTool.simple_glazing_cons(model, "Glazing_East", 2.2, 0.2697, 0.6)
glazing_west = ConstructionTool.simple_glazing_cons(model, "Glazing_West", 2.2, 0.261, 0.6)
glazing_north = ConstructionTool.simple_glazing_cons(model, "Glazing_North", 2.2, 0.1436, 0.6)
glazing_south = ConstructionTool.simple_glazing_cons(model, "Glazing_South", 2.2, 0.261, 0.6)

glazing_east_b = ConstructionTool.simple_glazing_cons(model, "Glazing_East", 2.2, 0.3, 0.6)
glazing_west_b = ConstructionTool.simple_glazing_cons(model, "Glazing_West", 2.2, 0.35, 0.6)
glazing_north_b = ConstructionTool.simple_glazing_cons(model, "Glazing_North", 2.2, 0.35, 0.6)
glazing_south_b = ConstructionTool.simple_glazing_cons(model, "Glazing_South", 2.2, 0.3, 0.6)

internal_mass_cons = ConstructionTool.opaque_cons(model, "Std Wood 6inch", 0.15, 0.12, 540, 1210, 3)

# Internal Load:
# **************************************************************************************
load_and_space = InternalLoad.internal_load_from_file("D:\\Projects\\OpenStudioDev\\LoadInputs.xlsx", "SHBank")
load = load_and_space[0]
space_list = load_and_space[1]

# Schedules:
# **************************************************************************************
schedule_sets = add_schedules(model, space_list)
# schedule_sets = schedule_sets_office(model)

# Load geometry from Rhino:
# **************************************************************************************
file_path = load_rhino_model(rhino_model_path, project_name, building_name)
geometries = GeometryTool.geometry_from_json(model, file_path, load, cons_set_b, schedule_sets, internal_mass_cons)

# Get all thermal zones for HVAC arrangement:
# **************************************************************************************
thermal_zones = geometries[0]
for zone in thermal_zones:
    if "Office" in zone["name"]:
        zone["zone"].setUseIdealAirLoads(True)

# Get all fenestration surfaces for construction assignment:
# **************************************************************************************
windows = geometries[2]
ZoneTool.construction_by_orientation(
    windows, glazing_east_b, glazing_west_b, glazing_north_b, glazing_south_b)

# Simulation settings:
# **************************************************************************************
SimulationSettingTool.set_timestep(model, 1)
SimulationSettingTool.heat_balance_algorithm(model, 500)

# Set output variables if any:
# **************************************************************************************
# output_variables(model, ["Heating Coil Heating Energy"])

# Save the model to the pre-defined path:
# **************************************************************************************
model.save(path, True)
print("Model is Ready!")
