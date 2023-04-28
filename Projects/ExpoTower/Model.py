from Constructions.ConstructionTools import ConstructionTool
from Schedules.Template import schedule_sets_office
from Schedules.ScheduleTools import ScheduleSets, ScheduleTool
from Resources.Models import create_model
from Resources.InternalLoad import InternalLoad
from RhinoGeometry.RhinoParse import load_rhino_model


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
geometries = GeometryTool.geometry_from_json(model, file_path, load)

# Save the model to the pre-defined path:
# **************************************************************************************
# model.save(path, True)
