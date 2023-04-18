import rhinoinside
rhinoinside.load()
try:
    import Rhino
except ImportError as e:
    raise ImportError("Failed to import Rhino.\n{}".format(e))

rhino_file_path = "D:\\Projects\\OpenStudioDev\\RhinoGeometry\\unit_test.3dm"
doc = Rhino.RhinoDoc.OpenHeadless(rhino_file_path)

unit1 = doc.GetUnitSystemName(True, True, True, False)

new_unit = Rhino.UnitSystem.Millimeters
doc.AdjustModelUnitSystem(new_unit, False)

unit2 = doc.GetUnitSystemName(True, True, True, False)

model = Rhino.FileIO.File3dm.Read(rhino_file_path)
Rhino.DocObjects.RhinoObject()

for obj in model.Objects:
    geometry = obj.Geometry
    bbx = geometry.GetBoundingBox(False)
    print(str(bbx.Max.Z) + ", " + str(bbx.Min.Z))

# print(unit2)
