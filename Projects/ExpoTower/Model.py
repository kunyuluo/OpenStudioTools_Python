import openstudio
from Geometry.GeometryTools import GeometryTool
from SiteAndLocation.SiteTools import SiteLocationTool
from SimulationSettings.SimulationSettings import SimulationSettingTool
from Constructions.ConstructionTools import ConstructionTool

# Create a new openstudio model
# **************************************************************************************
model = openstudio.openstudiomodel.Model()

# File Path:
# **************************************************************************************
path_str = "D:\\Projects\\OpenStudioDev\\ExpoTower.osm"
path = openstudio.openstudioutilitiescore.toPath(path_str)

# Create a building in the model:
# **************************************************************************************
building = GeometryTool.building(model, "Expo Tower", 0)

# Weather file:
# **************************************************************************************
epw_path_str = "D:\\Projects\\OpenStudioDev\\CHN_Shanghai.Shanghai.583670_IWEC.epw"
ddy_path_str = "D:\\Projects\\OpenStudioDev\\CHN_Shanghai.Shanghai.583670_IWEC.ddy"

SiteLocationTool.set_weather_file(model, epw_path_str)
SiteLocationTool.set_site_and_design_days(model, ddy_path_str)

# Run period:
# **************************************************************************************
SimulationSettingTool.set_run_period(model)
SimulationSettingTool.simulation_controls(model, "FullExterior")

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


# Save the model to the pre-defined path:
# **************************************************************************************
# model.save(path, True)
vec = openstudio.openstudioutilitiesgeometry.Vector3d(1, 10, 0)
orient = GeometryTool.check_orientation(vec)
print(orient)
