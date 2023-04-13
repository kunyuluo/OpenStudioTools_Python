from RhinoParse import sort_geometry_from_rhino, building_dict, write_to_json

path = "D:\\Projects\\OpenStudioDev\\RhinoGeometry\\geometry_test.3dm"

all_geos = sort_geometry_from_rhino(path)

rooms = all_geos[0]
room_names = all_geos[3]
windows = all_geos[1]
shades = all_geos[2]

building = building_dict(rooms, room_names, windows, shades, "Kunyu_House")
write_to_json(building)
