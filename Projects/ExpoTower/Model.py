from Constructions.ConstructionTools import ConstructionTool
from Schedules.Template import schedule_sets_office
from Schedules.ScheduleTools import ScheduleSets, ScheduleTool
from Resources.Models import create_model
from Resources.InternalLoad import InternalLoad
from RhinoGeometry.RhinoParse import load_rhino_model, find_child_surface
from Geometry.GeometryTools import GeometryTool
from Resources.ZoneTools import ZoneTool
from Resources.Helpers import Helper
from HVACSystem.Template.Template import Template
from Projects.ExpoTower.Systems import hvac_system

# Weather file:
# **************************************************************************************
epw_path_str = "D:\\Projects\\OpenStudioDev\\CHN_Shanghai.Shanghai.583670_IWEC.epw"
ddy_path_str = "D:\\Projects\\OpenStudioDev\\CHN_Shanghai.Shanghai.583670_IWEC.ddy"
path_str = "D:\\Projects\\OpenStudioDev\\ExpoTower.osm"
#
# # Create a new openstudio model
# # **************************************************************************************
model_file = create_model(epw_path_str, ddy_path_str, path_str, "Expo Tower")
model = model_file[0]
path = model_file[1]

# Construction set:
# **************************************************************************************
cons_set_1F = ConstructionTool.construction_set_simple(
    model, "1-4F Construction Set", False, 0.58, 0.43, 0.55, 2.2, 0.45, 0.6, 0.57, 0.43, 0.55, 0.57, 0.43, 0.55)

cons_set_5F = ConstructionTool.construction_set_simple(
    model, "5F Construction Set", False, 0.57, 0.43, 0.55, 2.14, 0.36, 0.6, 0.57, 0.43, 0.55, 0.57, 0.43, 0.55)

glazing_east_5F = ConstructionTool.simple_glazing_cons(model, "Glazing_East_5F", 2.14, 0.36, 0.6)
glazing_west_5F = ConstructionTool.simple_glazing_cons(model, "Glazing_West_5F", 1.93, 0.33, 0.6)
glazing_north_5F = ConstructionTool.simple_glazing_cons(model, "Glazing_North_5F", 2.15, 0.36, 0.6)
glazing_south_5F = ConstructionTool.simple_glazing_cons(model, "Glazing_South_5F", 1.93, 0.32, 0.6)

ext_wall_east = ConstructionTool.opaque_no_mass_cons(model, "East R-15 Wall", Helper.r_ip_to_si(15))
ext_wall_south = ConstructionTool.opaque_no_mass_cons(model, "South R-19 Wall", Helper.r_ip_to_si(19))

# Schedules:
# **************************************************************************************
schedule_template = schedule_sets_office(model)

schedule_1 = ScheduleSets(model)
schedule_1.set_occupancy(schedule=schedule_template["occupancy"])
schedule_1.set_lighting(schedule=schedule_template["lighting"])
schedule_1.set_electric_equipment(schedule=schedule_template["electric_equipment"])
schedule_1.set_infiltration(schedule=schedule_template["infiltration"])
schedule_1.set_cooling_setpoint(schedule=schedule_template["cooling_setpoint"])
schedule_1.set_heating_setpoint(schedule=schedule_template["heating_setpoint"])

# Internal Load:
# **************************************************************************************
space_types = ["Restroom", "Stair", "Elevator", "Electrical", "ElevatorLobby", "Office_Pri_1", "Office_Pri_2",
               "Office_Pri_3", "Office_Pri_4", "Office_Int_1", "Office_Int_2", "Office_Int_3", "Office_Int_4",
               "Cafeteria_1F", "Cafeteria_Pri_1", "Cafeteria_Pri_2", "Cafeteria_Pri_3", "Cafeteria_Pri_4",
               "Cafeteria_Int_1", "Cafeteria_Int_2", "Cafeteria_Int_3", "Cafeteria_Int_4", "Lobby", "Corridor",
               "Exhibition"]

load = InternalLoad.internal_load_input_json(
    ["Office", "Conference", "Corridor"],
    [0.8, 1.3, 0.6],
    [1.2, 1.8, 0.5],
    [0.1, 0.3, 0.05],
    [200, 200, 200],
    [0.15, 0.15, 0.15],
    [0.2, 0.2, 0.2],
    [3, 1, 3])

# Load geometry from Rhino:
# **************************************************************************************
file_path = load_rhino_model("D:\\Projects\\OpenStudioDev\\RhinoGeometry\\geometry_test.3dm", "Kunyu_House")
geometries = GeometryTool.geometry_from_json(model, file_path, load, cons_set_1F, schedule_1)

# Get all thermal zones for HVAC arrangement:
# **************************************************************************************
thermal_zones = geometries[0]
# sorted_zones = ZoneTool.thermal_zone_by_floor(thermal_zones, True)

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
# Template.vav_chiller_boiler(model, ZoneTool.get_thermal_zone(thermal_zones), air_loop_dehumidification_control=True,
#                             number_of_chiller=2, chiller_cop=6.8, chiller_condenser_type=2)

# Save the model to the pre-defined path:
# **************************************************************************************
model.save(path, True)
