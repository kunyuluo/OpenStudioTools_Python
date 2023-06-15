from Constructions.ConstructionTools import ConstructionTool
from Schedules.ScheduleTools import ScheduleSets, ScheduleTool
from Resources.Models import create_model
from Resources.InternalLoad import InternalLoad
from RhinoGeometry.RhinoParse import load_rhino_model
from Geometry.GeometryTools import GeometryTool
from Resources.ZoneTools import ZoneTool
from Resources.Helpers import Helper
from Projects.BoxModel.Systems import hvac_system
from Projects.BoxModel.Schedule import add_schedules
from OutputData.OutputData import output_variables

# Weather file:
# **************************************************************************************
epw_path_str = "D:\\Projects\\OpenStudioDev\\CHN_Shanghai.Shanghai.583670_IWEC.epw"
ddy_path_str = "D:\\Projects\\OpenStudioDev\\CHN_Shanghai.Shanghai.583670_IWEC.ddy"
path_str = "D:\\Projects\\OpenStudioDev\\Test_Model.osm"
#
# # Create a new openstudio model
# # **************************************************************************************
model_file = create_model(epw_path_str, ddy_path_str, path_str, "Test Building", north_axis=0)
model = model_file[0]
path = model_file[1]

# Construction set:
# **************************************************************************************
cons_set = ConstructionTool.construction_set_simple(
    model, "Test Construction Set", False, 0.58, 0.43, 0.55, 2.2, 0.45, 0.6, 0.57, 0.43, 0.57, 0.43, 0.55)

glazing_east = ConstructionTool.simple_glazing_cons(model, "Glazing_East", 2.14, 0.36, 0.6)
glazing_west = ConstructionTool.simple_glazing_cons(model, "Glazing_West", 1.93, 0.33, 0.6)
glazing_north = ConstructionTool.simple_glazing_cons(model, "Glazing_North", 2.15, 0.36, 0.6)
glazing_south = ConstructionTool.simple_glazing_cons(model, "Glazing_South", 1.93, 0.32, 0.6)

ext_wall_east = ConstructionTool.opaque_no_mass_cons(model, "East R-15 Wall", Helper.r_ip_to_si(15))
ext_wall_south = ConstructionTool.opaque_no_mass_cons(model, "South R-19 Wall", Helper.r_ip_to_si(19))

# Internal Load:
# **************************************************************************************
load_and_space = InternalLoad.internal_load_from_file("D:\\Projects\\OpenStudioDev\\LoadInputs.xlsx", "BoxModel")
load = load_and_space[0]
space_list = load_and_space[1]

# Schedules:
# **************************************************************************************
schedule_sets = add_schedules(model, space_list)
# print(schedule_sets["OpenOffice_1W"].get_schedule_sets())

# Load geometry from Rhino:
# **************************************************************************************
file_path = load_rhino_model("D:\\Projects\\OpenStudioDev\\RhinoGeometry\\BoxModel.3dm", "Kunyu_House")
geometries = GeometryTool.geometry_from_json(model, file_path, load, cons_set, schedule_sets)

# Get all thermal zones for HVAC arrangement:
# **************************************************************************************
thermal_zones = geometries[0]
# sorted_zones = ZoneTool.thermal_zone_by_floor(thermal_zones, True)

# Get all exterior wall surfaces for construction assignment:
# **************************************************************************************
ext_walls = geometries[1]
ZoneTool.construction_by_orientation(ext_walls, construction_east=ext_wall_east, construction_south=ext_wall_south)

# Get all fenestration surfaces for construction assignment:
# **************************************************************************************
windows = geometries[2]
ZoneTool.construction_by_orientation(windows, glazing_east, glazing_west, glazing_north, glazing_south)

# Build HVAC system:
# **************************************************************************************
hvac_system(model, thermal_zones)

# Set output variables if any:
# **************************************************************************************
output_variables(model, ["Zone Air Temperature", "Zone Air Relative Humidity", "Zone Air Humidity Ratio"])

# Save the model to the pre-defined path:
# **************************************************************************************
model.save(path, True)
