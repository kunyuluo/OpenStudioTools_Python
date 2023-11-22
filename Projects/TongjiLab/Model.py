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
import json

# Project Info:
# **************************************************************************************
project_name = "TongjiLab"
building_name = "TongjiLab"
rhino_model_path = "D:\\Projects\\OpenStudioDev\\RhinoGeometry\\Lab.3dm"

# Weather file:
# **************************************************************************************
epw_path_str = "D:\\Projects\\OpenStudioDev\\CHN_Shanghai.Shanghai.583670_IWEC.epw"
path_str = "D:\\Projects\\OpenStudioDev\\Tongji_Lab.osm"

# Create a new openstudio model
# **************************************************************************************
wall_orientation = 40
model_file = create_model(epw_path_str, path_str, "Tongji_Lab", north_axis=wall_orientation)
model = model_file[0]
path = model_file[1]

# Construction set:
# **************************************************************************************
ext_wall_u_value = 0.72
ext_roof_u_value = 0.43
ext_floor_u_value = 0.55
win_u_value = 3.3
win_shgc = 0.45
win_trans = 0.6
int_wall_u_value = 1.66
int_floor_u_floor = 0.43

cons_set_1 = ConstructionTool.construction_set_simple(
    model, "Construction Set", False, ext_wall_u_value, ext_roof_u_value, ext_floor_u_value,
    win_u_value, win_shgc, win_trans, int_wall_u_value, int_floor_u_floor, 0.57, 0.43, 0.55)

internal_mass_cons = ConstructionTool.opaque_cons(model, "Std Wood 6inch", 0.15, 0.12, 540, 1210, 3)

# Internal Load:
# **************************************************************************************
# load_and_space = InternalLoad.internal_load_from_file("D:\\Projects\\OpenStudioDev\\LoadInputs.xlsx", "Tongji_Lab")
# load = load_and_space[0]
# space_list = load_and_space[1]
lab_area = 31.9548
number_of_equipment = 1
unit_equipment_power = 200
number_of_light = 1
unit_light_power = 200
number_of_people = 4
outdoor_air_per_person = 30  # m3/h
people_latent_heat = 69  # w
people_sensible_heat = 112  # w

load = {
    "Office": {
        "conditioned": False,
        "lighting": 8,
        "equipment": 3.09,
        "people_density": 15.82,
        "people_density_method": "Area/Person",
        "people_activity_level": 181,
        "outdoor_air_per_area": 0,
        "outdoor_air_per_person": 0.00833333333333333,
        "gas_power": None,
        "internal_mass_area": 3,
        "internal_mass_method": "SurfaceArea/Area"
    },
    "Lab": {
        "conditioned": True,
        "lighting": unit_light_power * number_of_light / lab_area,
        "equipment": unit_equipment_power * number_of_equipment / lab_area,
        "people_density": number_of_people,
        "people_density_method": "People",
        "people_activity_level": people_sensible_heat + people_latent_heat,
        "outdoor_air_per_area": 0,
        "outdoor_air_per_person": outdoor_air_per_person / 3600,
        "gas_power": None,
        "internal_mass_area": 3,
        "internal_mass_method": "SurfaceArea/Area"
    },
    "Mech": {
        "conditioned": False,
        "lighting": 8,
        "equipment": 3.09,
        "people_density": 15.82,
        "people_density_method": "Area/Person",
        "people_activity_level": 181,
        "outdoor_air_per_area": 0,
        "outdoor_air_per_person": 0.00333333333333333,
        "gas_power": None,
        "internal_mass_area": 3,
        "internal_mass_method": "SurfaceArea/Area"
    },
    "Others": {
        "conditioned": False,
        "lighting": 0,
        "equipment": 0.0,
        "people_density": 1000.0,
        "people_density_method": "Area/Person",
        "people_activity_level": 181,
        "outdoor_air_per_area": 0,
        "outdoor_air_per_person": 0.0,
        "gas_power": None,
        "internal_mass_area": 3,
        "internal_mass_method": "SurfaceArea/Area"
    }
}
space_list = ['Office', 'Lab', 'Mech', 'Others']
load = json.dumps(load, indent=4)
print(load)

# Schedules:
# **************************************************************************************
schedule_sets = add_schedules(model, space_list, people_sensible_heat + people_latent_heat)

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
start_month = 1
start_day = 1
end_month = 12
end_day = 31

SimulationSettingTool.set_run_period(model, start_month, start_day, end_month, end_day)
SimulationSettingTool.set_timestep(model, 1)
SimulationSettingTool.heat_balance_algorithm(model, 500)

# Set output variables if any:
# **************************************************************************************
# output_variables(model, ["Zone Ideal Loads Supply Air Total Cooling Energy", "Zone Ideal Loads Supply Air Total Heating Energy"])

# Save the model to the pre-defined path:
# **************************************************************************************
# model.save(path, True)
print("Model is Ready!")

