import openstudio.openstudiomodelgeometry
from openstudio import *
from openstudio.openstudiomodel import Model, Building
from openstudio.openstudioutilitiesgeometry import Point3d, Vector3d, Plane
from Geometry.GeometryTools import GeometryTool
from SiteAndLocation.SiteTools import SiteLocationTool


# vertices = []
path_str = "D:\Projects\OpenStudioDev\Model_350.osm"
newPath_str = "D:\Projects\OpenStudioDev\Model_2.osm"
# newPath_str = "D:\Projects\OpenStudioDev\Model_gbxml.xml"
path = openstudioutilitiescore.toPath(path_str)
newPath = openstudioutilitiescore.toPath(newPath_str)

epw_path_str = "D:\Projects\OpenStudioDev\OpenStudio_Tools\OpenStudioTools_Python\OSW\CHN_Beijing.Beijing.545110_IWEC.epw"

ddy_path_str = "D:\Projects\OpenStudioDev\CHN_Shanghai.Shanghai.583670_IWEC.ddy"
ddy_path = openstudio.openstudioutilitiescore.toPath(ddy_path_str)

model = Model.load(path).get()
building = model.getBuilding()
building.setName("Building 1")
print(building.name())
# openstudio.gbxml.GbXMLForwardTranslator().modelToGbXML(model, newPath)

# Weather file:
SiteLocationTool.set_weather_file(model, epw_path_str)

# Site and design days:
SiteLocationTool.set_site_and_design_days(model, ddy_path_str)

# Geometry tool testing:
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
origin = Point3d(0,0,0)
normal = Vector3d(0,0,1)
plane = Plane(origin,normal)
# print(plane.outwardNormal())

# print("result = " + str(sch.scheduleRules()))
model.save(newPath, True)
