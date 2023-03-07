from openstudio import *
from openstudio.openstudiomodel import Model, Building
from openstudio.openstudioutilitiesgeometry import Point3d, Vector3d, Plane
from Geometry.GeometryTools import GeometryTool


# vertices = []
path_str = "D:\Projects\OpenStudioDev\Model_350.osm"
newPath_str = "D:\Projects\OpenStudioDev\Model_2.osm"
# newPath_str = "D:\Projects\OpenStudioDev\Model_gbxml.xml"
path = openstudioutilitiescore.toPath(path_str)
newPath = openstudioutilitiescore.toPath(newPath_str)

model = Model.load(path).get()
building = model.getBuilding()
building.setName("Building 1")
print(building.name())
# openstudio.gbxml.GbXMLForwardTranslator().modelToGbXML(model, newPath)

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
# model.save(newPath, True)

# p = os.path.abspath("myFile.txt")
# folder = os.path.dirname(p)
# print(folder)
#
# print(str(pathlib.Path(__file__).parent.absolute()/ "output" / "test_output.osm"))