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
from Schedules.Templates.Office import Office


# vertices = []
path_str = "D:\Projects\OpenStudioDev\Model_350.osm"
newPath_str = "D:\Projects\OpenStudioDev\Model_2.osm"
# newPath_str = "D:\Projects\OpenStudioDev\Model_gbxml.xml"
path = openstudioutilitiescore.toPath(path_str)
newPath = openstudioutilitiescore.toPath(newPath_str)

epw_path_str = "D:\Projects\OpenStudioDev\OpenStudio_Tools\OpenStudioTools_Python\OSW\CHN_Beijing.Beijing.545110_IWEC.epw"

ddy_path_str = "D:\Projects\OpenStudioDev\CHN_Shanghai.Shanghai.583670_IWEC.ddy"
ddy_path = openstudioutilitiescore.toPath(ddy_path_str)

# Get the model:
# **************************************************************************************
model = Model.load(path).get()
building = model.getBuilding()
building.setName("Kunyu's House")
print(building.name())
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
space_1 = ZoneTool.space_simplified(
    model,
    name="Kunyu's room",
    program="Office",
    lighting_power=0.7,
    equipment_power=1.5,
    people_density=10,
    outdoor_air_per_person=0.05,
    outdoor_air_per_floor_area=0.15,
    lighting_schedule=office_sch.lighting(),
    equipment_schedule=office_sch.equipment(),
    occupancy_schedule=office_sch.occupancy(),
    activity_schedule=office_sch.activity_level(),
    infiltration_schedule=office_sch.infiltration())

# Load Definition:
# **************************************************************************************
InternalLoad.add_lights(model, space_1, lighting_power=3.75, lighting_schedule=office_sch.lighting())
InternalLoad.add_people(
    model,
    space_1,
    amount=2.3,
    schedule=office_sch.occupancy(),
    activity_schedule=office_sch.activity_level(),
    enable_ashrae55_warning=True,
    mrt_calc_type="SurfaceWeighted",
    thermal_comfort_model_type=["AdaptiveASH55", "KSU"])

# Geometry tool testing:
# **************************************************************************************
vertices_1 = [[0.0, 0.0, 0.0], [5.0, 0.0, 0.0], [5.0, 0.0, 3.0], [0.0, 0.0, 3.0]]
wall_1 = GeometryTool.make_surface(model, vertices_1)

vertices_2 = [[0.0, 0.0, 0.0], [0.0, 0.0, 3.0], [5.0, 0.0, 3.0], [5.0, 0.0, 0.0]]
wall_2 = GeometryTool.make_surface(model, vertices_2)

vertices_3 = [[0.0, 4.0, 0.0], [0.0, 4.0, 3.0], [5.0, 4.0, 3.0], [5.0, 4.0, 0.0]]
wall_3 = GeometryTool.make_surface(model, vertices_3)

vertices_4 = [[0.0, 9.0, 0.0], [0.0, 9.0, 3.0], [5.0, 9.0, 3.0], [5.0, 9.0, 0.0]]
wall_4 = GeometryTool.make_surface(model, vertices_4)

walls = [wall_1, wall_2, wall_3, wall_4]
GeometryTool.solve_adjacency(walls, True)

wall_show = wall_4
print(wall_show.surfaceType() + "," + wall_show.outsideBoundaryCondition())
print(wall_show.outwardNormal())


# Plane Testing:
# **************************************************************************************
origin = Point3d(0,0,0)
normal = Vector3d(0,0,1)
plane = Plane(origin,normal)
# print(plane.outwardNormal())

# **************************************************************************************
# print("result = " + str(sch.scheduleRules()))
# model.save(newPath, True)
